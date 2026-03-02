"""Upload a local image or video asset, then publish it as a pin."""

from __future__ import annotations

import os

from _common import (
    account_label,
    make_sync_client,
    new_idempotency_key,
    prepare_media_source,
    resolve_account,
    resolve_board_id,
    run_sync_example,
)
from pinbridge_sdk.models import PinCreate


def main() -> int:
    with make_sync_client(require_api_key=True) as client:
        account = resolve_account(client)
        board_id = resolve_board_id(client, account.id)
        media = prepare_media_source(client)
        pin = client.pins.create(
            PinCreate(
                account_id=account.id,
                board_id=board_id,
                title=os.getenv("PINBRIDGE_PIN_TITLE", "PinBridge SDK local media example"),
                description=os.getenv("PINBRIDGE_PIN_DESCRIPTION"),
                link_url=os.getenv("PINBRIDGE_LINK_URL"),
                asset_id=media.asset_id,
                image_url=media.image_url,
                idempotency_key=new_idempotency_key("sdk-local-media"),
            )
        )
        job = client.jobs.get(pin.id)

    print(f"Account: {account_label(account)}")
    print(f"Board: {board_id}")
    print(f"Media source: {media.source_label}")
    print(f"Pin queued: id={pin.id} status={pin.status.value}")
    print(f"Job status: {job.status.value}")
    return 0


if __name__ == "__main__":
    run_sync_example(main)
