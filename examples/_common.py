"""Shared helpers for PinBridge SDK examples."""

from __future__ import annotations

import asyncio
import os
import sys
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from mimetypes import guess_type
from pathlib import Path
from typing import Awaitable, Callable
from uuid import UUID, uuid4

from pinbridge_sdk import APIError, AsyncPinbridgeClient, PinbridgeClient
from pinbridge_sdk.models import LoginRequest, PinterestAccountResponse

DEFAULT_BASE_URL = "https://api.pinbridge.io"

SyncMain = Callable[[], int]
AsyncMain = Callable[[], Awaitable[int]]


@dataclass(frozen=True)
class MediaSelection:
    asset_id: UUID | None
    image_url: str | None
    source_label: str


def required_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value


def env_flag(name: str, default: bool = False) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def env_int(name: str, default: int) -> int:
    value = os.getenv(name)
    return int(value) if value else default


def timestamp_name(prefix: str) -> str:
    return f"{prefix} {datetime.now(UTC):%Y%m%d-%H%M%S}"


def schedule_time(minutes: int | None = None) -> datetime:
    resolved_minutes = minutes if minutes is not None else env_int("PINBRIDGE_SCHEDULE_MINUTES", 60)
    return datetime.now(UTC) + timedelta(minutes=resolved_minutes)


def make_sync_client(*, require_api_key: bool = False) -> PinbridgeClient:
    api_key = (
        required_env("PINBRIDGE_API_KEY") if require_api_key else os.getenv("PINBRIDGE_API_KEY")
    )
    base_url = os.getenv("PINBRIDGE_BASE_URL", DEFAULT_BASE_URL)
    return PinbridgeClient(base_url=base_url, api_key=api_key)


def make_async_client(*, require_api_key: bool = False) -> AsyncPinbridgeClient:
    api_key = (
        required_env("PINBRIDGE_API_KEY") if require_api_key else os.getenv("PINBRIDGE_API_KEY")
    )
    base_url = os.getenv("PINBRIDGE_BASE_URL", DEFAULT_BASE_URL)
    return AsyncPinbridgeClient(base_url=base_url, api_key=api_key)


def login_with_env(client: PinbridgeClient) -> str:
    auth = client.auth.login(
        LoginRequest(
            email=required_env("PINBRIDGE_EMAIL"),
            password=required_env("PINBRIDGE_PASSWORD"),
        )
    )
    client.set_bearer_token(auth.access_token)
    return auth.access_token


async def async_login_with_env(client: AsyncPinbridgeClient) -> str:
    auth = await client.auth.login(
        LoginRequest(
            email=required_env("PINBRIDGE_EMAIL"),
            password=required_env("PINBRIDGE_PASSWORD"),
        )
    )
    client.set_bearer_token(auth.access_token)
    return auth.access_token


def resolve_account(client: PinbridgeClient) -> PinterestAccountResponse:
    requested_id = os.getenv("PINBRIDGE_ACCOUNT_ID")
    accounts = client.pinterest.list_accounts()
    if not accounts:
        oauth = client.pinterest.start_oauth()
        raise RuntimeError(
            "No connected Pinterest account found. Connect one first via "
            f"{oauth.authorization_url}"
        )

    if requested_id:
        for account in accounts:
            if str(account.id) == requested_id:
                return account
        raise RuntimeError(f"PINBRIDGE_ACCOUNT_ID={requested_id} was not found.")

    return accounts[0]


async def resolve_account_async(client: AsyncPinbridgeClient) -> PinterestAccountResponse:
    requested_id = os.getenv("PINBRIDGE_ACCOUNT_ID")
    accounts = await client.pinterest.list_accounts()
    if not accounts:
        oauth = await client.pinterest.start_oauth()
        raise RuntimeError(
            "No connected Pinterest account found. Connect one first via "
            f"{oauth.authorization_url}"
        )

    if requested_id:
        for account in accounts:
            if str(account.id) == requested_id:
                return account
        raise RuntimeError(f"PINBRIDGE_ACCOUNT_ID={requested_id} was not found.")

    return accounts[0]


def resolve_board_id(client: PinbridgeClient, account_id: UUID | str) -> str:
    requested_id = os.getenv("PINBRIDGE_BOARD_ID")
    boards = client.pinterest.list_boards(account_id)
    if not boards:
        raise RuntimeError(
            "No boards found for the selected account. Create one first or set PINBRIDGE_BOARD_ID."
        )

    if requested_id:
        for board in boards:
            if board.id == requested_id:
                return board.id
        raise RuntimeError(f"PINBRIDGE_BOARD_ID={requested_id} was not found.")

    return boards[0].id


async def resolve_board_id_async(client: AsyncPinbridgeClient, account_id: UUID | str) -> str:
    requested_id = os.getenv("PINBRIDGE_BOARD_ID")
    boards = await client.pinterest.list_boards(account_id)
    if not boards:
        raise RuntimeError(
            "No boards found for the selected account. Create one first or set PINBRIDGE_BOARD_ID."
        )

    if requested_id:
        for board in boards:
            if board.id == requested_id:
                return board.id
        raise RuntimeError(f"PINBRIDGE_BOARD_ID={requested_id} was not found.")

    return boards[0].id


def account_label(account: PinterestAccountResponse) -> str:
    return account.display_name or account.username or account.pinterest_user_id


def new_idempotency_key(prefix: str) -> str:
    return f"{prefix}-{uuid4()}"


def _content_type_for_path(path: str) -> str:
    return guess_type(path)[0] or "application/octet-stream"


def upload_local_asset(client: PinbridgeClient) -> MediaSelection:
    image_path = os.getenv("PINBRIDGE_IMAGE_PATH")
    video_path = os.getenv("PINBRIDGE_VIDEO_PATH")
    if bool(image_path) == bool(video_path):
        raise RuntimeError("Set exactly one of PINBRIDGE_IMAGE_PATH or PINBRIDGE_VIDEO_PATH")

    if image_path:
        asset = client.assets.upload_image(
            image_path, content_type=_content_type_for_path(image_path)
        )
        return MediaSelection(
            asset_id=asset.id,
            image_url=None,
            source_label=f"uploaded image {Path(image_path).name}",
        )

    asset = client.assets.upload_video(video_path, content_type=_content_type_for_path(video_path))
    return MediaSelection(
        asset_id=asset.id, image_url=None, source_label=f"uploaded video {Path(video_path).name}"
    )


async def upload_local_asset_async(client: AsyncPinbridgeClient) -> MediaSelection:
    image_path = os.getenv("PINBRIDGE_IMAGE_PATH")
    video_path = os.getenv("PINBRIDGE_VIDEO_PATH")
    if bool(image_path) == bool(video_path):
        raise RuntimeError("Set exactly one of PINBRIDGE_IMAGE_PATH or PINBRIDGE_VIDEO_PATH")

    if image_path:
        asset = await client.assets.upload_image(
            image_path,
            content_type=_content_type_for_path(image_path),
        )
        return MediaSelection(
            asset_id=asset.id,
            image_url=None,
            source_label=f"uploaded image {Path(image_path).name}",
        )

    asset = await client.assets.upload_video(
        video_path,
        content_type=_content_type_for_path(video_path),
    )
    return MediaSelection(
        asset_id=asset.id, image_url=None, source_label=f"uploaded video {Path(video_path).name}"
    )


def prepare_media_source(client: PinbridgeClient) -> MediaSelection:
    image_url = os.getenv("PINBRIDGE_IMAGE_URL")
    image_path = os.getenv("PINBRIDGE_IMAGE_PATH")
    video_path = os.getenv("PINBRIDGE_VIDEO_PATH")
    selected = [value for value in (image_url, image_path, video_path) if value]
    if len(selected) != 1:
        raise RuntimeError(
            "Set exactly one of PINBRIDGE_IMAGE_URL, PINBRIDGE_IMAGE_PATH, or PINBRIDGE_VIDEO_PATH"
        )
    if image_url:
        return MediaSelection(asset_id=None, image_url=image_url, source_label="hosted image URL")
    return upload_local_asset(client)


async def prepare_media_source_async(client: AsyncPinbridgeClient) -> MediaSelection:
    image_url = os.getenv("PINBRIDGE_IMAGE_URL")
    image_path = os.getenv("PINBRIDGE_IMAGE_PATH")
    video_path = os.getenv("PINBRIDGE_VIDEO_PATH")
    selected = [value for value in (image_url, image_path, video_path) if value]
    if len(selected) != 1:
        raise RuntimeError(
            "Set exactly one of PINBRIDGE_IMAGE_URL, PINBRIDGE_IMAGE_PATH, or PINBRIDGE_VIDEO_PATH"
        )
    if image_url:
        return MediaSelection(asset_id=None, image_url=image_url, source_label="hosted image URL")
    return await upload_local_asset_async(client)


def run_sync_example(main: SyncMain) -> None:
    try:
        raise SystemExit(main())
    except APIError as exc:
        print(f"API error [{exc.status_code}] {exc.message}", file=sys.stderr)
        raise SystemExit(2) from exc
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        raise SystemExit(3) from exc


def run_async_example(main: AsyncMain) -> None:
    try:
        raise SystemExit(asyncio.run(main()))
    except APIError as exc:
        print(f"API error [{exc.status_code}] {exc.message}", file=sys.stderr)
        raise SystemExit(2) from exc
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        raise SystemExit(3) from exc
