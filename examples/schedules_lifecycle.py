"""Create, inspect, list, and optionally cancel a scheduled pin."""

from __future__ import annotations

import os

from _common import (
    account_label,
    env_flag,
    make_sync_client,
    prepare_media_source,
    resolve_account,
    resolve_board_id,
    run_sync_example,
    schedule_time,
)
from pinbridge_sdk.models import ScheduleCreate


def main() -> int:
    with make_sync_client(require_api_key=True) as client:
        account = resolve_account(client)
        board_id = resolve_board_id(client, account.id)
        media = prepare_media_source(client)
        schedule = client.schedules.create(
            ScheduleCreate(
                account_id=account.id,
                run_at=schedule_time(),
                board_id=board_id,
                title=os.getenv("PINBRIDGE_SCHEDULED_PIN_TITLE", "PinBridge SDK scheduled example"),
                description=os.getenv("PINBRIDGE_SCHEDULED_PIN_DESCRIPTION"),
                link_url=os.getenv("PINBRIDGE_LINK_URL"),
                asset_id=media.asset_id,
                image_url=media.image_url,
            )
        )
        fetched = client.schedules.get(schedule.id)
        recent = client.schedules.list(limit=5)

        if env_flag("PINBRIDGE_CANCEL_SCHEDULE"):
            canceled = client.schedules.cancel(schedule.id)
            cancel_status = canceled.status.value
        else:
            cancel_status = "skipped"

    print(f"Account: {account_label(account)}")
    print(f"Board: {board_id}")
    print(f"Media source: {media.source_label}")
    print(f"Created schedule: id={schedule.id} run_at={schedule.run_at.isoformat()}")
    print(f"Fetched schedule status: {fetched.status.value}")
    print(f"Recent schedules returned: {len(recent)}")
    print(f"Cancel step: {cancel_status}")
    return 0


if __name__ == "__main__":
    run_sync_example(main)
