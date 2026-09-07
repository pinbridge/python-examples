"""Manage organization team members and invitations.

Demonstrates the team resource added to the SDK: listing members and invitations,
creating/resending/revoking an invitation, and updating a member's role.

Requires a user session (email/password), because team management is scoped to the
signed-in user's organization. Invite target and role come from the environment:
``PINBRIDGE_INVITE_EMAIL`` (default teammate@example.com) and ``PINBRIDGE_INVITE_ROLE``
(default ``editor``). Mutations run only when ``PINBRIDGE_MANAGE_TEAM=1``.
"""

from __future__ import annotations

import os

from _common import env_flag, login_with_env, make_sync_client, run_sync_example
from pinbridge_sdk.models import TeamInvitationCreateRequest, TeamMemberUpdateRequest


def main() -> int:
    with make_sync_client() as client:
        login_with_env(client)

        members = client.team.list_members()
        print(f"Team members: {len(members.items)}")

        invitations = client.team.list_invitations()
        print(f"Pending invitations: {len(invitations.items)}")

        if not env_flag("PINBRIDGE_MANAGE_TEAM"):
            print("Management steps: skipped (set PINBRIDGE_MANAGE_TEAM=1 to enable)")
            return 0

        invite = client.team.create_invitation(
            TeamInvitationCreateRequest(
                email=os.getenv("PINBRIDGE_INVITE_EMAIL", "teammate@example.com"),
                role=os.getenv("PINBRIDGE_INVITE_ROLE", "editor"),
            )
        )
        print(f"Created invitation: id={invite.id} email={invite.email} role={invite.role}")

        resent = client.team.resend_invitation(invite.id)
        print(f"Resent invitation: id={resent.id}")

        if members.items:
            member = members.items[0]
            updated = client.team.update_member(
                member.id, TeamMemberUpdateRequest(role=member.role)
            )
            print(f"Updated member: id={updated.id} role={updated.role}")

        revoked = client.team.revoke_invitation(invite.id)
        print(f"Revoked invitation: {revoked.message}")
    return 0


if __name__ == "__main__":
    run_sync_example(main)
