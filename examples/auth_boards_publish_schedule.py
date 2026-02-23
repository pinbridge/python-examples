"""End-to-end PinBridge SDK example:
1) Authenticate
2) List boards
3) Create board
4) Publish pin
5) Schedule pin
"""

from __future__ import annotations

import os
import sys
from datetime import UTC, datetime, timedelta
from uuid import uuid4

from pinbridge_sdk import APIError, PinbridgeClient
from pinbridge_sdk.models import (
    BoardCreateRequest,
    LoginRequest,
    PinCreate,
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
    image_url = _required_env("PINBRIDGE_IMAGE_URL")

    link_url = os.getenv("PINBRIDGE_LINK_URL")
    account_id_override = os.getenv("PINBRIDGE_ACCOUNT_ID")

    now = datetime.now(UTC)
    board_name = os.getenv("PINBRIDGE_BOARD_NAME", f"SDK Example {now:%Y%m%d-%H%M%S}")
    board_description = os.getenv(
        "PINBRIDGE_BOARD_DESCRIPTION", "Created from PinBridge Python SDK"
    )
    board_privacy = os.getenv("PINBRIDGE_BOARD_PRIVACY")

    pin_title = os.getenv("PINBRIDGE_PIN_TITLE", "My SDK Published Pin")
    pin_description = os.getenv(
        "PINBRIDGE_PIN_DESCRIPTION", "Published via PinBridge Python SDK"
    )
    scheduled_pin_title = os.getenv(
        "PINBRIDGE_SCHEDULED_PIN_TITLE", "My SDK Scheduled Pin"
    )
    scheduled_pin_description = os.getenv(
        "PINBRIDGE_SCHEDULED_PIN_DESCRIPTION",
        "Scheduled via PinBridge Python SDK",
    )
    schedule_minutes = int(os.getenv("PINBRIDGE_SCHEDULE_MINUTES", "60"))

    with PinbridgeClient(base_url=base_url) as client:
        print("Authenticating...")
        auth = client.auth.login(LoginRequest(email=email, password=password))
        client.set_bearer_token(auth.access_token)
        print(
            f"Authenticated as {auth.user.email} in workspace '{auth.workspace.name}'"
        )

        accounts = client.pinterest.list_accounts()
        if not accounts:
            oauth = client.pinterest.start_oauth()
            print("No connected Pinterest account found.")
            print("Connect one account first using this URL, then rerun this script:")
            print(oauth.authorization_url)
            return 1

        if account_id_override:
            account = next(
                (a for a in accounts if str(a.id) == account_id_override), None
            )
            if account is None:
                raise RuntimeError(
                    f"PINBRIDGE_ACCOUNT_ID={account_id_override} was not found in connected accounts."
                )
        else:
            account = accounts[0]
        print(
            f"Using Pinterest account: {account.id} ({account.display_name or account.username})"
        )

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

        print("Publishing a pin...")
        published_pin = client.pins.create(
            PinCreate(
                account_id=account.id,
                board_id=new_board.id,
                title=pin_title,
                description=pin_description,
                link_url=link_url,
                image_url=image_url,
                idempotency_key=f"sdk-publish-{uuid4()}",
            )
        )
        print(
            f"Published pin request accepted: {published_pin.id} status={published_pin.status.value}"
        )

        print("Scheduling a pin...")
        schedule = client.schedules.create(
            ScheduleCreate(
                account_id=account.id,
                run_at=datetime.now(UTC) + timedelta(minutes=schedule_minutes),
                board_id=new_board.id,
                title=scheduled_pin_title,
                description=scheduled_pin_description,
                link_url=link_url,
                image_url=image_url,
            )
        )
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
