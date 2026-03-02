"""Advanced SDK patterns: with_options, low-level requests, and custom resources."""

from __future__ import annotations

import json

from _common import make_sync_client, run_sync_example
from pinbridge_sdk.resources.base import SyncAPIResource


class DiagnosticsResource(SyncAPIResource):
    def ping(self) -> str:
        response = self._request("GET", "/healthz")
        return json.loads(response.content.decode("utf-8"))["status"]


def main() -> int:
    with make_sync_client(require_api_key=True) as client:
        derived = client.with_options(headers={"x-request-source": "python-examples"})
        raw_health = derived.request("GET", "/healthz").json()
        print(f"Derived client health: {raw_health['status']}")

        client.register_resource("diagnostics", DiagnosticsResource)
        status = client.diagnostics.ping()  # type: ignore[attr-defined]
        print(f"Custom resource ping: {status}")

        root = client.system.root()
        print(f"Root docs URL: {root.docs}")

    return 0


if __name__ == "__main__":
    run_sync_example(main)
