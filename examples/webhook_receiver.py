"""Run a small local webhook receiver that verifies PinBridge signatures."""

from __future__ import annotations

import json
import os
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Any

from webhook_signature_verification import verify_webhook_signature


def verify_delivery(
    headers: dict[str, str],
    body: bytes,
    *,
    secret: str,
) -> tuple[bool, dict[str, Any]]:
    signature = headers.get("X-PinBridge-Signature", "")
    event = headers.get("X-PinBridge-Event", "unknown")
    delivery_id = headers.get("X-PinBridge-Delivery-ID", "unknown")
    is_valid = verify_webhook_signature(body, signature, secret)

    try:
        payload = json.loads(body.decode("utf-8"))
    except json.JSONDecodeError:
        payload = {"raw_body": body.decode("utf-8", errors="replace")}

    return is_valid, {
        "event": event,
        "delivery_id": delivery_id,
        "payload": payload,
    }


class _WebhookHandler(BaseHTTPRequestHandler):
    webhook_secret = ""

    def do_POST(self) -> None:  # noqa: N802
        content_length = int(self.headers.get("Content-Length", "0"))
        body = self.rfile.read(content_length)
        headers = {key: value for key, value in self.headers.items()}
        is_valid, details = verify_delivery(headers, body, secret=self.webhook_secret)

        if not is_valid:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"invalid signature")
            return

        print(
            f"Received {details['event']} delivery_id={details['delivery_id']} "
            f"payload={json.dumps(details['payload'], sort_keys=True)}"
        )
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"ok")

    def log_message(self, format: str, *args: object) -> None:  # noqa: A003
        return


def main() -> int:
    secret = os.getenv("PINBRIDGE_WEBHOOK_SECRET")
    if not secret:
        raise RuntimeError("Set PINBRIDGE_WEBHOOK_SECRET before starting the local receiver")

    host = os.getenv("PINBRIDGE_WEBHOOK_HOST", "127.0.0.1")
    port = int(os.getenv("PINBRIDGE_WEBHOOK_PORT", "8787"))

    _WebhookHandler.webhook_secret = secret
    server = HTTPServer((host, port), _WebhookHandler)
    print(f"Listening on http://{host}:{port}/ for PinBridge webhooks")
    print("Press Ctrl+C to stop.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down receiver")
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
