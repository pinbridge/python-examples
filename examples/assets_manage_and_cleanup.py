"""List workspace assets and clean up storage with single and bulk deletes.

Demonstrates the asset-management surface added to the SDK:
``client.assets.list``, ``client.assets.delete`` (with confirmation handling), and
``client.assets.bulk_delete``.

Deletions only run when ``PINBRIDGE_DELETE_ASSETS=1`` so the example is safe to run
read-only by default.
"""

from __future__ import annotations

from _common import env_flag, make_sync_client, run_sync_example


def main() -> int:
    with make_sync_client(require_api_key=True) as client:
        listing = client.assets.list(limit=50)
        print(f"Assets: {len(listing.assets)} of {listing.total}")
        print(
            f"Storage: {listing.storage_used_bytes}/{listing.storage_quota_bytes} bytes "
            f"({listing.storage_used_percent}%)"
        )

        if not listing.assets:
            print("No assets to clean up.")
            return 0

        target = listing.assets[0]
        print(f"First asset: id={target.id} filename={target.original_filename}")

        if not env_flag("PINBRIDGE_DELETE_ASSETS"):
            print("Delete step: skipped (set PINBRIDGE_DELETE_ASSETS=1 to enable)")
            return 0

        # A referenced asset needs confirm=True; delete() reports when confirmation is required.
        result = client.assets.delete(target.id, confirm=True)
        print(
            f"Deleted asset: deleted={result.deleted} "
            f"freed_bytes={result.freed_bytes} referenced_pins={result.referenced_pin_count}"
        )

        bulk = client.assets.bulk_delete([target.id], confirm=True)
        print(
            f"Bulk delete: deleted={len(bulk.deleted)} "
            f"needs_confirmation={len(bulk.requires_confirmation)} "
            f"freed_bytes={bulk.total_freed_bytes}"
        )
    return 0


if __name__ == "__main__":
    run_sync_example(main)
