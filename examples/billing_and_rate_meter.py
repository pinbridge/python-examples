"""Inspect pricing, billing status, and rate-meter capacity."""

from __future__ import annotations

from _common import (
    account_label,
    env_flag,
    login_with_env,
    make_sync_client,
    resolve_account,
    run_sync_example,
)


def main() -> int:
    with make_sync_client() as client:
        login_with_env(client)

        pricing = client.billing.pricing()
        status = client.billing.status()

        print(f"Pricing source: {pricing.source}")
        print(f"Plans available: {len(pricing.plans)}")
        print(f"Current plan: {status.plan.value}")
        print(f"Billing status: {status.billing_status.value}")
        print(f"Calls used this month: {status.calls_used}/{status.quota_calls_monthly}")

        try:
            account = resolve_account(client)
        except RuntimeError as exc:
            print(f"Skipping rate-meter lookup: {exc}")
            account = None

        if account is not None:
            meter = client.rate_meter.get(account.id)
            print(f"Rate meter account: {account_label(account)}")
            print(
                "Account tokens: "
                f"{meter.account.tokens_available:.2f}/{meter.account.capacity:.2f}"
            )
            print(
                "Global tokens: "
                f"{meter.global_.tokens_available:.2f}/{meter.global_.capacity:.2f}"
            )

        if env_flag("PINBRIDGE_CREATE_PORTAL"):
            portal = client.billing.portal()
            print(f"Customer portal URL: {portal.url}")
        else:
            print("Skipping billing portal creation. Set PINBRIDGE_CREATE_PORTAL=1 to include it.")

    return 0


if __name__ == "__main__":
    run_sync_example(main)
