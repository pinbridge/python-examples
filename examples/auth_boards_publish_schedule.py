"""End-to-end PinBridge SDK example:
1) Authenticate
2) List boards
3) Create board
4) Upload local media asset
5) Publish pin
6) Schedule pin
"""

from __future__ import annotations

import os
import sys
from datetime import UTC, datetime, timedelta
from mimetypes import guess_type
from uuid import uuid4

from pinbridge_sdk import APIError, PinbridgeClient
from pinbridge_sdk.models import (
    BoardCreateRequest,
    LoginRequest,
    PinCreate,
    ProjectResponse,
    ScheduleCreate,
)


def _required_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value


def main() -> int:
    base_url = os.getenv("PINBRIDGE_BASE_URL", "https://api.pinbridge.io")
    email = _required_env("PINBRIDGE_EMAIL")
    password = _required_env("PINBRIDGE_PASSWORD")
    image_path = os.getenv("PINBRIDGE_IMAGE_PATH")
    video_path = os.getenv("PINBRIDGE_VIDEO_PATH")
    image_url = os.getenv("PINBRIDGE_IMAGE_URL")
    if not image_path and not video_path and not image_url:
        raise RuntimeError("Set PINBRIDGE_IMAGE_PATH, PINBRIDGE_VIDEO_PATH, or PINBRIDGE_IMAGE_URL")
    if image_path and video_path:
        raise RuntimeError("Set only one of PINBRIDGE_IMAGE_PATH or PINBRIDGE_VIDEO_PATH")

    link_url = os.getenv("PINBRIDGE_LINK_URL")
    account_id_override = os.getenv("PINBRIDGE_ACCOUNT_ID")

    now = datetime.now(UTC)
    board_name = os.getenv("PINBRIDGE_BOARD_NAME", f"SDK Example {now:%Y%m%d-%H%M%S}")
    board_description = os.getenv(
        "PINBRIDGE_BOARD_DESCRIPTION", "Created from PinBridge Python SDK"
    )
    board_privacy = os.getenv("PINBRIDGE_BOARD_PRIVACY")

    pin_title = os.getenv("PINBRIDGE_PIN_TITLE", "My SDK Published Pin")
    pin_description = os.getenv("PINBRIDGE_PIN_DESCRIPTION", "Published via PinBridge Python SDK")
    scheduled_pin_title = os.getenv("PINBRIDGE_SCHEDULED_PIN_TITLE", "My SDK Scheduled Pin")
    scheduled_pin_description = os.getenv(
        "PINBRIDGE_SCHEDULED_PIN_DESCRIPTION",
        "Scheduled via PinBridge Python SDK",
    )
    schedule_minutes = int(os.getenv("PINBRIDGE_SCHEDULE_MINUTES", "60"))
    project_mode = os.getenv("PINBRIDGE_PROJECT_MODE", "production").strip().lower()
    if project_mode not in {"production", "sandbox"}:
        raise RuntimeError("PINBRIDGE_PROJECT_MODE must be 'production' or 'sandbox'")

    with PinbridgeClient(base_url=base_url) as client:
        print("Authenticating...")
        auth = client.auth.login(LoginRequest(email=email, password=password))
        client.set_bearer_token(auth.access_token)
        print(f"Authenticated as {auth.user.email} in workspace '{auth.workspace.name}'")

        if project_mode == "sandbox":
            context = client.projects.list()
            sandbox_project: ProjectResponse | None = next(
                (project for project in context.projects if project.environment.value == "sandbox"),
                None,
            )
            if sandbox_project is None:
                context = client.projects.create_sandbox()
                sandbox_project = next(
                    (
                        project
                        for project in context.projects
                        if project.environment.value == "sandbox"
                    ),
                    None,
                )
            if sandbox_project is None:
                raise RuntimeError("Failed to create or find sandbox project")

            switch_result = client.projects.switch({"project_id": str(sandbox_project.id)})
            client.set_bearer_token(switch_result.access_token)
            print(f"Switched to sandbox project: {sandbox_project.id} ({sandbox_project.name})")

        accounts = client.pinterest.list_accounts()
        if not accounts:
            oauth = client.pinterest.start_oauth()
            print("No connected Pinterest account found.")
            print("Connect one account first using this URL, then rerun this script:")
            print(oauth.authorization_url)
            return 1

        if account_id_override:
            account = next((a for a in accounts if str(a.id) == account_id_override), None)
            if account is None:
                raise RuntimeError(
                    f"PINBRIDGE_ACCOUNT_ID={account_id_override} was not found in connected accounts."
                )
        else:
            account = accounts[0]
        print(f"Using Pinterest account: {account.id} ({account.display_name or account.username})")

        print("Listing boards...")
        boards = client.pinterest.list_boards(account.id)
        print(f"Found {len(boards)} existing board(s).")
        for board in boards[:5]:
            print(f"- {board.id}: {board.name}")

        print("Creating a board...")
        new_board = client.pinterest.create_board(
            BoardCreateRequest(
                account_id=account.id,
                name=board_name,
                description=board_description,
                privacy=board_privacy,
            )
        )
        print(f"Created board: {new_board.id} ({new_board.name})")

        asset_id = None
        if image_path:
            print("Uploading image asset...")
            guessed_content_type = guess_type(image_path)[0] or "application/octet-stream"
            asset = client.assets.upload_image(image_path, content_type=guessed_content_type)
            asset_id = asset.id
            print(f"Uploaded asset: {asset.id}")
        elif video_path:
            print("Uploading video asset...")
            guessed_content_type = guess_type(video_path)[0] or "application/octet-stream"
            asset = client.assets.upload_video(video_path, content_type=guessed_content_type)
            asset_id = asset.id
            print(f"Uploaded asset: {asset.id}")

        print("Publishing a pin...")
        pin_payload = PinCreate(
            account_id=account.id,
            board_id=new_board.id,
            title=pin_title,
            description=pin_description,
            link_url=link_url,
            asset_id=asset_id,
            image_url=image_url,
            idempotency_key=f"sdk-publish-{uuid4()}",
        )
        published_pin = client.pins.create(pin_payload)
        print(
            f"Published pin request accepted: {published_pin.id} status={published_pin.status.value}"
        )

        print("Scheduling a pin...")
        schedule_payload = ScheduleCreate(
            account_id=account.id,
            run_at=datetime.now(UTC) + timedelta(minutes=schedule_minutes),
            board_id=new_board.id,
            title=scheduled_pin_title,
            description=scheduled_pin_description,
            link_url=link_url,
            asset_id=asset_id,
            image_url=image_url,
        )
        schedule = client.schedules.create(schedule_payload)
        print(f"Created schedule: {schedule.id} run_at={schedule.run_at.isoformat()}")

    print("Done.")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except APIError as exc:
        print(f"API error [{exc.status_code}] {exc.message}", file=sys.stderr)
        raise SystemExit(2) from exc
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        raise SystemExit(3) from exc
