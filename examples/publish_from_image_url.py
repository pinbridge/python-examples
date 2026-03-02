"""Publish a pin using an already-hosted image URL."""

from __future__ import annotations

import os

from _common import (
    account_label,
    make_sync_client,
    new_idempotency_key,
    required_env,
    resolve_account,
    resolve_board_id,
    run_sync_example,
)
from pinbridge_sdk.models import PinCreate


def main() -> int:
    with make_sync_client(require_api_key=True) as client:
        account = resolve_account(client)
        board_id = resolve_board_id(client, account.id)
        pin = client.pins.create(
            PinCreate(
                account_id=account.id,
                board_id=board_id,
                title=required_env("PINBRIDGE_PIN_TITLE"),
                description=os.getenv("PINBRIDGE_PIN_DESCRIPTION"),
                link_url=os.getenv("PINBRIDGE_LINK_URL"),
                image_url=required_env("PINBRIDGE_IMAGE_URL"),
                idempotency_key=new_idempotency_key("sdk-image-url"),
            )
        )
        fetched = client.pins.get(pin.id)
        job = client.jobs.get(pin.id)

    print(f"Account: {account_label(account)}")
    print(f"Board: {board_id}")
    print(f"Pin queued: id={pin.id} status={pin.status.value}")
    print(f"Pin fetch: status={fetched.status.value} media_url={fetched.media_url}")
    print(f"Job status: {job.status.value}")
    return 0


if __name__ == "__main__":
    run_sync_example(main)
