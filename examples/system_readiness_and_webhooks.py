"""Check readiness and optionally forward a Stripe webhook payload."""

from __future__ import annotations

from _common import env_flag, make_sync_client, required_env, run_sync_example


def main() -> int:
    with make_sync_client() as client:
        readiness = client.system.readiness()
        print(
            f"Readiness: status={readiness.status} "
            f"environment={readiness.environment} database={readiness.database}"
        )

        if env_flag("PINBRIDGE_FORWARD_STRIPE_WEBHOOK"):
            result = client.system.stripe_webhook(
                required_env("PINBRIDGE_STRIPE_WEBHOOK_BODY"),
                stripe_signature=required_env("PINBRIDGE_STRIPE_SIGNATURE"),
            )
            print(f"Stripe webhook forwarded: {result.get('status', 'ok')}")
        else:
            print(
                "Skipping Stripe webhook forward. "
                "Set PINBRIDGE_FORWARD_STRIPE_WEBHOOK=1 to include it."
            )

    return 0


if __name__ == "__main__":
    run_sync_example(main)
