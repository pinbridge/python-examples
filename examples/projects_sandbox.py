"""Inspect projects, ensure a sandbox exists, and optionally reset it."""

from __future__ import annotations

from _common import env_flag, login_with_env, make_sync_client, run_sync_example


def main() -> int:
    with make_sync_client() as client:
        login_with_env(client)

        context = client.projects.list()
        print(f"Organization: {context.organization.name}")
        print(
            f"Active project: {context.active_project.name} ({context.active_project.environment.value})"
        )

        sandbox = next(
            (project for project in context.projects if project.environment.value == "sandbox"),
            None,
        )
        if sandbox is None:
            context = client.projects.create_sandbox()
            sandbox = next(
                (project for project in context.projects if project.environment.value == "sandbox"),
                None,
            )
            if sandbox is None:
                raise RuntimeError("Sandbox creation did not return a sandbox project")
            print(f"Created sandbox project: {sandbox.id} ({sandbox.name})")
        else:
            print(f"Found existing sandbox project: {sandbox.id} ({sandbox.name})")

        switched = client.projects.switch({"project_id": str(sandbox.id)})
        client.set_bearer_token(switched.access_token)
        print(f"Switched active project to sandbox: {switched.active_project.name}")

        if env_flag("PINBRIDGE_RESET_SANDBOX"):
            reset = client.projects.reset_sandbox()
            print(f"Sandbox reset complete for project: {reset.active_project.name}")
        else:
            print("Skipping sandbox reset. Set PINBRIDGE_RESET_SANDBOX=1 to include it.")

    return 0


if __name__ == "__main__":
    run_sync_example(main)
