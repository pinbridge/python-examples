"""Authenticate with bearer auth and inspect workspace profile state."""

from __future__ import annotations

from _common import login_with_env, make_sync_client, run_sync_example


def main() -> int:
    with make_sync_client() as client:
        login_with_env(client)
        me = client.auth.me()
        profile = client.auth.get_profile()

        print(f"Authenticated as: {me.user.email}")
        print(f"Organization: {me.organization.name}")
        print(f"Active project: {me.active_project.name} ({me.active_project.environment.value})")
        print(f"Workspace profile: {profile.workspace_name}")
        print(f"Billing email: {profile.billing_email or 'not set'}")

        for project in me.projects:
            print(
                f"- project={project.name} env={project.environment.value} plan={project.plan.value}"
            )

    return 0


if __name__ == "__main__":
    run_sync_example(main)
