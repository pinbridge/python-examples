"""List Pinterest accounts and boards, with optional board create/delete steps."""

from __future__ import annotations

import os

from _common import (
    account_label,
    env_flag,
    login_with_env,
    make_sync_client,
    run_sync_example,
    timestamp_name,
)
from pinbridge_sdk.models import BoardCreateRequest


def main() -> int:
    with make_sync_client() as client:
        login_with_env(client)

        accounts = client.pinterest.list_accounts()
        if not accounts:
            oauth = client.pinterest.start_oauth()
            print("No connected Pinterest account found.")
            print(f"Start OAuth here: {oauth.authorization_url}")
            return 1

        print(f"Connected Pinterest accounts: {len(accounts)}")
        account = accounts[0]
        print(f"Using account: {account.id} ({account_label(account)})")

        boards = client.pinterest.list_boards(account.id)
        print(f"Boards found: {len(boards)}")
        for board in boards[:10]:
            print(f"- {board.id}: {board.name}")

        if not env_flag("PINBRIDGE_CREATE_BOARD"):
            print(
                "Skipping board creation. Set PINBRIDGE_CREATE_BOARD=1 to create a temporary board."
            )
            return 0

        created = client.pinterest.create_board(
            BoardCreateRequest(
                account_id=account.id,
                name=os.getenv("PINBRIDGE_BOARD_NAME", timestamp_name("SDK example board")),
                description=os.getenv(
                    "PINBRIDGE_BOARD_DESCRIPTION", "Created by the Python SDK examples"
                ),
                privacy=os.getenv("PINBRIDGE_BOARD_PRIVACY"),
            )
        )
        print(f"Created board: {created.id} ({created.name})")

        if env_flag("PINBRIDGE_DELETE_CREATED_BOARD"):
            client.pinterest.delete_board(created.id, account_id=account.id)
            print("Deleted the created board")
        else:
            print("Keeping the created board. Set PINBRIDGE_DELETE_CREATED_BOARD=1 to delete it.")

    return 0


if __name__ == "__main__":
    run_sync_example(main)
