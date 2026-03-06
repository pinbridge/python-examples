"""Create/list/delete pins and run JSON/CSV bulk import jobs."""

from __future__ import annotations

from _common import (
    env_flag,
    make_sync_client,
    new_idempotency_key,
    required_env,
    resolve_account,
    resolve_board_id,
    run_sync_example,
    schedule_time,
)
from pinbridge_sdk.models import PinCreate, PinImportCreate


def main() -> int:
    with make_sync_client(require_api_key=True) as client:
        account = resolve_account(client)
        board_id = resolve_board_id(client, account.id)
        image_url = required_env("PINBRIDGE_IMAGE_URL")

        created = client.pins.create(
            PinCreate(
                account_id=account.id,
                board_id=board_id,
                title="SDK manage pin",
                description="Created by the bulk import example",
                image_url=image_url,
                idempotency_key=new_idempotency_key("sdk-manage-pin"),
            )
        )
        print(f"Created pin: {created.id} ({created.status.value})")

        listed = client.pins.list(limit=5)
        print(f"Pins listed: {len(listed)}")

        json_job = client.pins.import_json(
            [
                PinImportCreate(
                    account_id=account.id,
                    board_id=board_id,
                    title="JSON import row",
                    description="Imported from JSON payload",
                    image_url=image_url,
                    idempotency_key=new_idempotency_key("sdk-import-json"),
                    run_at=schedule_time(120),
                )
            ]
        )
        print(f"JSON import job: {json_job.id} ({json_job.status.value})")

        csv_payload = (
            "account_id,board_id,title,description,image_url,idempotency_key\n"
            f"{account.id},{board_id},CSV import row,Imported from CSV,{image_url},"
            f"{new_idempotency_key('sdk-import-csv')}\n"
        )
        csv_job = client.pins.import_csv(
            csv_payload.encode("utf-8"),
            filename="pins.csv",
            content_type="text/csv",
        )
        print(f"CSV import job: {csv_job.id} ({csv_job.status.value})")

        fetched_job = client.pins.get_import(json_job.id)
        recent_jobs = client.pins.list_imports(limit=5)
        print(f"Fetched import job status: {fetched_job.status.value}")
        print(f"Import jobs listed: {len(recent_jobs)}")

        if env_flag("PINBRIDGE_DELETE_CREATED_PIN"):
            client.pins.delete(created.id)
            print("Deleted the created pin")
        else:
            print("Skipping pin delete. Set PINBRIDGE_DELETE_CREATED_PIN=1 to include it.")

    return 0


if __name__ == "__main__":
    run_sync_example(main)
