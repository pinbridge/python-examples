"""Recipe: map a Shopify product launch into a PinBridge publish."""

from __future__ import annotations

import os

from _common import (
    account_label,
    make_sync_client,
    required_env,
    resolve_account,
    resolve_board_id,
    run_sync_example,
)
from pinbridge_sdk.models import PinCreate


def main() -> int:
    product_id = os.getenv("SHOPIFY_PRODUCT_ID", "shopify-demo-product")
    title = os.getenv("SHOPIFY_PRODUCT_TITLE", "Shopify launch pin")
    description = os.getenv(
        "SHOPIFY_PRODUCT_DESCRIPTION", "Published from a Shopify product update"
    )
    product_url = required_env("SHOPIFY_PRODUCT_URL")
    image_url = required_env("SHOPIFY_IMAGE_URL")

    with make_sync_client(require_api_key=True) as client:
        account = resolve_account(client)
        board_id = resolve_board_id(client, account.id)
        pin = client.pins.create(
            PinCreate(
                account_id=account.id,
                board_id=board_id,
                title=title,
                description=description,
                link_url=product_url,
                image_url=image_url,
                idempotency_key=f"shopify-product-{product_id}",
            )
        )

    print(f"Account: {account_label(account)}")
    print(f"Board: {board_id}")
    print(f"Published Shopify product pin: {pin.id} status={pin.status.value}")
    return 0


if __name__ == "__main__":
    run_sync_example(main)
