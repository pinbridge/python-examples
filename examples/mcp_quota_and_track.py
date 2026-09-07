"""Inspect and increment the workspace's weekly MCP request quota.

Demonstrates ``client.mcp.quota`` (read current usage) and ``client.mcp.track``
(increment the counter, as the MCP server does after a successful tool call).
The track step runs only when ``PINBRIDGE_TRACK_MCP=1``.
"""

from __future__ import annotations

from _common import env_flag, make_sync_client, run_sync_example


def main() -> int:
    with make_sync_client(require_api_key=True) as client:
        quota = client.mcp.quota()
        limit = "unlimited" if quota.requests_limit == 0 else str(quota.requests_limit)
        print(
            f"MCP quota ({quota.week}): used={quota.requests_used} limit={limit} "
            f"exhausted={quota.quota_exhausted} resets_at={quota.resets_at}"
        )

        if not env_flag("PINBRIDGE_TRACK_MCP"):
            print("Track step: skipped (set PINBRIDGE_TRACK_MCP=1 to enable)")
            return 0

        tracked = client.mcp.track()
        print(f"After track: used={tracked.requests_used} exhausted={tracked.quota_exhausted}")
    return 0


if __name__ == "__main__":
    run_sync_example(main)
