"""Retry a failed pin and run bulk retry/delete over existing pins.

Demonstrates the pin lifecycle methods added to the SDK: ``client.pins.retry``,
``client.pins.bulk_retry``, and ``client.pins.bulk_delete``. Bulk mutations return a
``BulkOperationResponse`` with per-item ``results`` (succeeded / skipped / failed).

Destructive steps are gated on ``PINBRIDGE_DELETE_PINS=1``.
"""

from __future__ import annotations

from _common import env_flag, make_sync_client, run_sync_example
from pinbridge_sdk.models import PinRetryRequest


def main() -> int:
    with make_sync_client(require_api_key=True) as client:
        pins = client.pins.list(limit=25)
        print(f"Pins fetched: {len(pins)}")
        if not pins:
            print("No pins to operate on.")
            return 0

        pin_ids = [pin.id for pin in pins]
        first = pins[0]

        # Retry a single pin, optionally redirecting it to a different board.
        retried = client.pins.retry(first.id, PinRetryRequest(board_id=first.board_id))
        print(f"Retried pin: id={retried.id} status={retried.status.value}")

        bulk_retry = client.pins.bulk_retry(pin_ids)
        print(
            f"Bulk retry: succeeded={bulk_retry.succeeded_count} "
            f"skipped={bulk_retry.skipped_count} failed={bulk_retry.failed_count}"
        )

        if env_flag("PINBRIDGE_DELETE_PINS"):
            bulk_delete = client.pins.bulk_delete(pin_ids)
            print(
                f"Bulk delete: succeeded={bulk_delete.succeeded_count} "
                f"failed={bulk_delete.failed_count}"
            )
        else:
            print("Bulk delete: skipped (set PINBRIDGE_DELETE_PINS=1 to enable)")
    return 0


if __name__ == "__main__":
    run_sync_example(main)
