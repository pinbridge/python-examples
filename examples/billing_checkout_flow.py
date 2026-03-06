"""Generate a Stripe checkout URL for a target plan/cycle."""

from __future__ import annotations

import os

from _common import login_with_env, make_sync_client, run_sync_example
from pinbridge_sdk.models import BillingCycle, CheckoutRequest, Plan


def _parse_plan(value: str) -> Plan:
    try:
        return Plan(value.strip().lower())
    except ValueError as exc:
        options = ", ".join(plan.value for plan in Plan)
        raise RuntimeError(
            f"Invalid PINBRIDGE_CHECKOUT_PLAN='{value}'. Use one of: {options}"
        ) from exc


def _parse_cycle(value: str) -> BillingCycle:
    try:
        return BillingCycle(value.strip().lower())
    except ValueError as exc:
        options = ", ".join(cycle.value for cycle in BillingCycle)
        raise RuntimeError(
            f"Invalid PINBRIDGE_CHECKOUT_CYCLE='{value}'. Use one of: {options}"
        ) from exc


def main() -> int:
    requested_plan = _parse_plan(os.getenv("PINBRIDGE_CHECKOUT_PLAN", "growth"))
    requested_cycle = _parse_cycle(os.getenv("PINBRIDGE_CHECKOUT_CYCLE", "monthly"))

    with make_sync_client() as client:
        login_with_env(client)
        checkout = client.billing.checkout(
            CheckoutRequest(plan=requested_plan, billing_cycle=requested_cycle)
        )

    print(f"Requested checkout: plan={requested_plan.value} cycle={requested_cycle.value}")
    print(f"Checkout URL: {checkout.url}")
    return 0


if __name__ == "__main__":
    run_sync_example(main)
