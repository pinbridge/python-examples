"""Show full auth/account lifecycle endpoints with safe opt-in mutations."""

from __future__ import annotations

import os

from _common import env_flag, login_with_env, make_sync_client, required_env, run_sync_example
from pinbridge_sdk.models import (
    ChangePasswordRequest,
    ForgotPasswordRequest,
    ProfileUpdateRequest,
    RegisterRequest,
    ResetPasswordRequest,
)


def authenticate(client) -> str:
    if not env_flag("PINBRIDGE_REGISTER_USER"):
        login_with_env(client)
        me = client.auth.me()
        print(f"Authenticated existing user: {me.user.email}")
        return me.user.email

    registered = client.auth.register(
        RegisterRequest(
            full_name=required_env("PINBRIDGE_REGISTER_FULL_NAME"),
            email=required_env("PINBRIDGE_REGISTER_EMAIL"),
            password=required_env("PINBRIDGE_REGISTER_PASSWORD"),
            workspace_name=os.getenv("PINBRIDGE_REGISTER_WORKSPACE_NAME"),
            timezone=os.getenv("PINBRIDGE_REGISTER_TIMEZONE"),
        )
    )
    client.set_bearer_token(registered.access_token)
    print(f"Registered new user: {registered.user.email}")
    return registered.user.email


def main() -> int:
    with make_sync_client() as client:
        email = authenticate(client)

        me = client.auth.me()
        profile = client.auth.get_profile()
        print(f"Workspace profile loaded: {profile.workspace_name}")
        print(f"Email verified: {me.user.email_verified}")

        if env_flag("PINBRIDGE_UPDATE_PROFILE"):
            updated = client.auth.update_profile(
                ProfileUpdateRequest(
                    full_name=os.getenv("PINBRIDGE_PROFILE_FULL_NAME"),
                    workspace_name=os.getenv("PINBRIDGE_PROFILE_WORKSPACE_NAME"),
                    company_name=os.getenv("PINBRIDGE_PROFILE_COMPANY_NAME", "PinBridge SDK"),
                    company_website=os.getenv("PINBRIDGE_PROFILE_COMPANY_WEBSITE"),
                    billing_email=os.getenv("PINBRIDGE_PROFILE_BILLING_EMAIL"),
                    billing_phone=os.getenv("PINBRIDGE_PROFILE_BILLING_PHONE"),
                )
            )
            print(f"Profile updated for workspace: {updated.workspace_name}")
        else:
            print("Skipping profile update. Set PINBRIDGE_UPDATE_PROFILE=1 to include it.")

        if env_flag("PINBRIDGE_REQUEST_EMAIL_VERIFICATION"):
            action = client.auth.request_email_verification()
            print(f"Email verification request: {action.message}")
        else:
            print(
                "Skipping email verification request. "
                "Set PINBRIDGE_REQUEST_EMAIL_VERIFICATION=1 to include it."
            )

        verification_token = os.getenv("PINBRIDGE_EMAIL_VERIFICATION_TOKEN")
        if verification_token:
            action = client.auth.verify_email(verification_token)
            print(f"Email verification result: {action.message}")
        else:
            print(
                "Skipping token verification. Set PINBRIDGE_EMAIL_VERIFICATION_TOKEN to include it."
            )

        if env_flag("PINBRIDGE_REQUEST_PASSWORD_RESET"):
            action = client.auth.forgot_password(ForgotPasswordRequest(email=email))
            print(f"Password reset request: {action.message}")
        else:
            print(
                "Skipping password reset request. "
                "Set PINBRIDGE_REQUEST_PASSWORD_RESET=1 to include it."
            )

        reset_token = os.getenv("PINBRIDGE_PASSWORD_RESET_TOKEN")
        new_password = os.getenv("PINBRIDGE_NEW_PASSWORD")
        if reset_token and new_password:
            action = client.auth.reset_password(
                ResetPasswordRequest(token=reset_token, password=new_password)
            )
            print(f"Password reset result: {action.message}")
        else:
            print(
                "Skipping password reset submit. "
                "Set PINBRIDGE_PASSWORD_RESET_TOKEN and PINBRIDGE_NEW_PASSWORD to include it."
            )

        if env_flag("PINBRIDGE_CHANGE_PASSWORD"):
            action = client.auth.change_password(
                ChangePasswordRequest(
                    current_password=required_env("PINBRIDGE_CURRENT_PASSWORD"),
                    new_password=required_env("PINBRIDGE_NEXT_PASSWORD"),
                )
            )
            print(f"Password change result: {action.message}")
        else:
            print("Skipping password change. Set PINBRIDGE_CHANGE_PASSWORD=1 to include it.")

    return 0


if __name__ == "__main__":
    run_sync_example(main)
