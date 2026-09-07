"""Manage scheduled pins with retry, delete and bulk operations.

Demonstrates the schedule lifecycle methods added to the SDK: ``client.schedules.retry``,
``client.schedules.delete``, ``client.schedules.bulk_cancel``,
``client.schedules.bulk_retry`` and ``client.schedules.bulk_delete``.

Mutating steps are gated on ``PINBRIDGE_MUTATE_SCHEDULES=1``.
"""

from __future__ import annotations

from _common import env_flag, make_sync_client, run_sync_example


def main() -> int:
    with make_sync_client(require_api_key=True) as client:
        schedules = client.schedules.list(limit=25)
        print(f"Schedules fetched: {len(schedules)}")
        if not schedules:
            print("No schedules to manage.")
            return 0

        schedule_ids = [schedule.id for schedule in schedules]
        first = schedules[0]

        if not env_flag("PINBRIDGE_MUTATE_SCHEDULES"):
            print("Mutation steps: skipped (set PINBRIDGE_MUTATE_SCHEDULES=1 to enable)")
            return 0

        retried = client.schedules.retry(first.id)
        print(f"Retried schedule: id={retried.id} status={retried.status.value}")

        canceled = client.schedules.bulk_cancel(schedule_ids)
        print(f"Bulk cancel: succeeded={canceled.succeeded_count} failed={canceled.failed_count}")

        requeued = client.schedules.bulk_retry(schedule_ids)
        print(f"Bulk retry: succeeded={requeued.succeeded_count} failed={requeued.failed_count}")

        deleted = client.schedules.bulk_delete(schedule_ids)
        print(f"Bulk delete: succeeded={deleted.succeeded_count} failed={deleted.failed_count}")

        client.schedules.delete(first.id)
        print(f"Deleted schedule: id={first.id}")
    return 0


if __name__ == "__main__":
    run_sync_example(main)
