"""Recipe: fan out a campaign pin to multiple connected Pinterest accounts."""

from __future__ import annotations

import os

from _common import (
    account_label,
    make_sync_client,
    new_idempotency_key,
    required_env,
    run_sync_example,
)
from pinbridge_sdk.models import PinCreate


def main() -> int:
    title = os.getenv("PINBRIDGE_PIN_TITLE", "Campaign launch")
    description = os.getenv("PINBRIDGE_PIN_DESCRIPTION", "Fan-out campaign publish")
    link_url = os.getenv("PINBRIDGE_LINK_URL")
    image_url = required_env("PINBRIDGE_IMAGE_URL")
    max_accounts = int(os.getenv("PINBRIDGE_MAX_ACCOUNTS", "3"))

    with make_sync_client(require_api_key=True) as client:
        accounts = client.pinterest.list_accounts()
        if not accounts:
            raise RuntimeError("No connected Pinterest accounts found")

        published = 0
        for account in accounts[:max_accounts]:
            boards = client.pinterest.list_boards(account.id)
            if not boards:
                print(f"Skipping {account_label(account)} because it has no boards")
                continue

            pin = client.pins.create(
                PinCreate(
                    account_id=account.id,
                    board_id=boards[0].id,
                    title=title,
                    description=description,
                    link_url=link_url,
                    image_url=image_url,
                    idempotency_key=new_idempotency_key(f"campaign-{account.id}"),
                )
            )
            print(
                f"Published to {account_label(account)} board={boards[0].id} "
                f"pin={pin.id} status={pin.status.value}"
            )
            published += 1

    print(f"Fan-out complete across {published} account(s)")
    return 0


if __name__ == "__main__":
    run_sync_example(main)
