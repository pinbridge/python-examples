"""Create, update, list, fetch, and delete a webhook endpoint."""

from __future__ import annotations

from _common import make_sync_client, required_env, run_sync_example
from pinbridge_sdk.models import WebhookCreate, WebhookUpdate


def main() -> int:
    with make_sync_client(require_api_key=True) as client:
        created = client.webhooks.create(
            WebhookCreate(
                url=required_env("PINBRIDGE_WEBHOOK_URL"),
                secret=required_env("PINBRIDGE_WEBHOOK_SECRET"),
                events=["pin.published", "pin.failed"],
            )
        )
        print(f"Created webhook: {created.id} -> {created.url}")

        updated = client.webhooks.update(
            created.id,
            WebhookUpdate(is_enabled=False),
        )
        print(f"Updated webhook enabled={updated.is_enabled}")

        fetched = client.webhooks.get(created.id)
        print(f"Fetched webhook events={','.join(fetched.events)}")

        listed = client.webhooks.list()
        print(f"Workspace webhook count: {len(listed)}")

        client.webhooks.delete(created.id)
        print("Deleted the example webhook")

    return 0


if __name__ == "__main__":
    run_sync_example(main)
