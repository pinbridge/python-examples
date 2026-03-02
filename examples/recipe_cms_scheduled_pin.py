"""Recipe: schedule a CMS article for Pinterest after editorial approval."""

from __future__ import annotations

import os

from _common import (
    account_label,
    make_sync_client,
    required_env,
    resolve_account,
    resolve_board_id,
    run_sync_example,
    schedule_time,
)
from pinbridge_sdk.models import ScheduleCreate


def main() -> int:
    article_slug = os.getenv("CMS_ARTICLE_SLUG", "cms-demo-article")
    title = os.getenv("CMS_ARTICLE_TITLE", "CMS article pin")
    description = os.getenv("CMS_ARTICLE_DESCRIPTION", "Scheduled from a CMS publish workflow")
    article_url = required_env("CMS_ARTICLE_URL")
    image_url = required_env("CMS_IMAGE_URL")

    with make_sync_client(require_api_key=True) as client:
        account = resolve_account(client)
        board_id = resolve_board_id(client, account.id)
        schedule = client.schedules.create(
            ScheduleCreate(
                account_id=account.id,
                board_id=board_id,
                run_at=schedule_time(),
                title=title,
                description=description,
                link_url=article_url,
                image_url=image_url,
            )
        )

    print(f"Account: {account_label(account)}")
    print(f"Board: {board_id}")
    print(f"Scheduled CMS article {article_slug}: {schedule.id} status={schedule.status.value}")
    return 0


if __name__ == "__main__":
    run_sync_example(main)
