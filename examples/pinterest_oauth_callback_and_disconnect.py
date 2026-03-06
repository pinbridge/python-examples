"""Demonstrate Pinterest OAuth callback handling and account revocation."""

from __future__ import annotations

import os

import httpx

from _common import env_flag, login_with_env, make_sync_client, run_sync_example


def main() -> int:
    with make_sync_client() as client:
        login_with_env(client)

        oauth_start = client.pinterest.start_oauth()
        print(f"OAuth start URL: {oauth_start.authorization_url}")

        oauth_code = os.getenv("PINBRIDGE_OAUTH_CODE")
        oauth_state = os.getenv("PINBRIDGE_OAUTH_STATE")
        if oauth_code and oauth_state:
            callback_result = client.pinterest.oauth_callback(
                code=oauth_code,
                state=oauth_state,
                follow_redirects=env_flag("PINBRIDGE_OAUTH_FOLLOW_REDIRECTS"),
            )
            if isinstance(callback_result, httpx.Response):
                location = callback_result.headers.get("location", "")
                print(
                    f"OAuth callback redirect: status={callback_result.status_code} "
                    f"location={location}"
                )
            else:
                print(
                    f"OAuth callback result: {callback_result.status} "
                    f"account_id={callback_result.account_id}"
                )
        else:
            print("Skipping OAuth callback. Set PINBRIDGE_OAUTH_CODE and PINBRIDGE_OAUTH_STATE.")

        accounts = client.pinterest.list_accounts()
        print(f"Connected accounts: {len(accounts)}")

        revoke_id = os.getenv("PINBRIDGE_REVOKE_ACCOUNT_ID")
        if not revoke_id and env_flag("PINBRIDGE_REVOKE_FIRST_ACCOUNT") and accounts:
            revoke_id = str(accounts[0].id)

        if revoke_id:
            client.pinterest.revoke_account(revoke_id)
            print(f"Revoked account: {revoke_id}")
        else:
            print(
                "Skipping account revoke. Set PINBRIDGE_REVOKE_ACCOUNT_ID "
                "or PINBRIDGE_REVOKE_FIRST_ACCOUNT=1."
            )

    return 0


if __name__ == "__main__":
    run_sync_example(main)
