"""Verify PinBridge webhook signatures locally."""

from __future__ import annotations

import hashlib
import hmac
import os

from _common import required_env, run_sync_example


def compute_webhook_signature(payload: bytes, secret: str) -> str:
    return hmac.new(secret.encode("utf-8"), payload, hashlib.sha256).hexdigest()


def verify_webhook_signature(payload: bytes, signature: str, secret: str) -> bool:
    expected = compute_webhook_signature(payload, secret)
    return hmac.compare_digest(expected, signature)


def main() -> int:
    secret = required_env("PINBRIDGE_WEBHOOK_SECRET")
    body = os.getenv("PINBRIDGE_WEBHOOK_BODY", '{"pin_id":"demo","status":"published"}').encode(
        "utf-8"
    )
    provided_signature = os.getenv("PINBRIDGE_WEBHOOK_SIGNATURE")

    expected_signature = compute_webhook_signature(body, secret)
    print(f"Expected signature: {expected_signature}")

    if not provided_signature:
        print(
            "No PINBRIDGE_WEBHOOK_SIGNATURE provided. Use the expected signature above to test verification."
        )
        return 0

    is_valid = verify_webhook_signature(body, provided_signature, secret)
    print(f"Provided signature valid: {is_valid}")
    return 0 if is_valid else 1


if __name__ == "__main__":
    run_sync_example(main)
