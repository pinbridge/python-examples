"""Basic connectivity checks for the PinBridge SDK."""

from __future__ import annotations

from _common import make_sync_client, run_sync_example


def main() -> int:
    with make_sync_client() as client:
        root = client.system.root()
        health = client.system.health()

    print(f"Service: {root.service}")
    print(f"Version: {root.version}")
    print(f"Docs: {root.docs}")
    print(
        "Health: "
        f"status={health.status} environment={health.environment} database={health.database}"
    )
    return 0


if __name__ == "__main__":
    run_sync_example(main)
