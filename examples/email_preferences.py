"""Read and update the signed-in user's email preferences.

Demonstrates ``client.email.get_preferences`` and ``client.email.update_preferences``.
Requires a user session (email/password). The update step runs only when
``PINBRIDGE_UPDATE_EMAIL_PREFERENCES=1``; the new values come from
``PINBRIDGE_EMAIL_TRANSACTIONAL`` / ``PINBRIDGE_EMAIL_ALERTS`` /
``PINBRIDGE_EMAIL_VERIFICATION`` (default: keep current values).
"""

from __future__ import annotations

from _common import env_flag, login_with_env, make_sync_client, run_sync_example
from pinbridge_sdk.models import EmailPreferencesUpdateRequest


def main() -> int:
    with make_sync_client() as client:
        login_with_env(client)

        prefs = client.email.get_preferences()
        print(
            "Current preferences: "
            f"transactional={prefs.transactional_enabled} "
            f"alerts={prefs.alerts_enabled} verification={prefs.verification_enabled}"
        )

        if not env_flag("PINBRIDGE_UPDATE_EMAIL_PREFERENCES"):
            print("Update step: skipped (set PINBRIDGE_UPDATE_EMAIL_PREFERENCES=1 to enable)")
            return 0

        updated = client.email.update_preferences(
            EmailPreferencesUpdateRequest(
                transactional_enabled=env_flag(
                    "PINBRIDGE_EMAIL_TRANSACTIONAL", prefs.transactional_enabled
                ),
                alerts_enabled=env_flag("PINBRIDGE_EMAIL_ALERTS", prefs.alerts_enabled),
                verification_enabled=env_flag(
                    "PINBRIDGE_EMAIL_VERIFICATION", prefs.verification_enabled
                ),
            )
        )
        print(
            "Updated preferences: "
            f"transactional={updated.transactional_enabled} "
            f"alerts={updated.alerts_enabled} verification={updated.verification_enabled}"
        )
    return 0


if __name__ == "__main__":
    run_sync_example(main)
