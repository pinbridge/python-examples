"""Async example for publishing a pin and scheduling another one."""

from __future__ import annotations

import asyncio
import os

from _common import (
    account_label,
    make_async_client,
    new_idempotency_key,
    prepare_media_source_async,
    resolve_account_async,
    resolve_board_id_async,
    run_async_example,
    schedule_time,
)
from pinbridge_sdk.models import PinCreate, ScheduleCreate


async def main() -> int:
    async with make_async_client(require_api_key=True) as client:
        account = await resolve_account_async(client)
        board_id = await resolve_board_id_async(client, account.id)
        media = await prepare_media_source_async(client)

        root, health = await asyncio.gather(client.system.root(), client.system.health())
        print(f"Connected to {root.service} version={root.version} health={health.status}")

        pin = await client.pins.create(
            PinCreate(
                account_id=account.id,
                board_id=board_id,
                title=os.getenv("PINBRIDGE_PIN_TITLE", "Async PinBridge pin"),
                description=os.getenv("PINBRIDGE_PIN_DESCRIPTION"),
                link_url=os.getenv("PINBRIDGE_LINK_URL"),
                asset_id=media.asset_id,
                image_url=media.image_url,
                idempotency_key=new_idempotency_key("sdk-async"),
            )
        )
        schedule = await client.schedules.create(
            ScheduleCreate(
                account_id=account.id,
                run_at=schedule_time(),
                board_id=board_id,
                title=os.getenv("PINBRIDGE_SCHEDULED_PIN_TITLE", "Async PinBridge schedule"),
                description=os.getenv("PINBRIDGE_SCHEDULED_PIN_DESCRIPTION"),
                link_url=os.getenv("PINBRIDGE_LINK_URL"),
                asset_id=media.asset_id,
                image_url=media.image_url,
            )
        )
        job = await client.jobs.get(pin.id)

    print(f"Account: {account_label(account)}")
    print(f"Board: {board_id}")
    print(f"Media source: {media.source_label}")
    print(f"Async pin status: {pin.status.value}")
    print(f"Async job status: {job.status.value}")
    print(f"Async schedule id: {schedule.id}")
    return 0


if __name__ == "__main__":
    run_async_example(main)
