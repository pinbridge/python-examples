"""Create, rotate metadata for, and revoke an API key."""

from __future__ import annotations

from _common import login_with_env, make_sync_client, run_sync_example, timestamp_name
from pinbridge_sdk.models import APIKeyCreate, APIKeyUpdate


def main() -> int:
    with make_sync_client() as client:
        login_with_env(client)

        created = client.api_keys.create(APIKeyCreate(name=timestamp_name("SDK example key")))
        print(f"Created API key id={created.id}")
        print(f"Secret (shown once): {created.api_key}")

        listed = client.api_keys.list()
        print(f"Workspace now has {len(listed)} API key record(s)")

        updated = client.api_keys.update(
            created.id,
            APIKeyUpdate(name=f"{created.name} rotated"),
        )
        print(f"Updated key name: {updated.name}")

        client.api_keys.revoke(created.id)
        print("Revoked the example key")

    return 0


if __name__ == "__main__":
    run_sync_example(main)
