from __future__ import annotations

import asyncio
import importlib

import httpx


UUID1 = "11111111-1111-1111-1111-111111111111"
UUID2 = "22222222-2222-2222-2222-222222222222"
UUID3 = "33333333-3333-3333-3333-333333333333"
UUID4 = "44444444-4444-4444-4444-444444444444"
UUID5 = "55555555-5555-5555-5555-555555555555"
UUID6 = "66666666-6666-6666-6666-666666666666"
TS = "2026-02-23T12:00:00Z"


def root_response() -> dict:
    return {"service": "PinBridge API", "version": "1.26.0", "docs": "/docs"}


def health_response() -> dict:
    return {
        "status": "ok",
        "version": "1.26.0",
        "environment": "test",
        "checks": {"database": "ok", "redis": "ok"},
    }


def readiness_response() -> dict:
    return {"status": "ok", "version": "1.26.0", "environment": "test", "database": "ok"}


def auth_workspace_response() -> dict:
    return {
        "id": UUID2,
        "name": "SDK Workspace",
        "environment": "production",
        "timezone": "UTC",
        "plan": "starter",
    }


def auth_user_response() -> dict:
    return {
        "id": UUID1,
        "email": "dev@pinbridge.io",
        "full_name": "SDK User",
        "timezone": "UTC",
        "email_verified": True,
        "created_at": TS,
    }


def auth_response() -> dict:
    workspace = auth_workspace_response()
    return {
        "access_token": "jwt-token",
        "token_type": "bearer",
        "expires_in": 3600,
        "user": auth_user_response(),
        "organization": {"id": UUID3, "name": "SDK Org"},
        "active_project": workspace,
        "projects": [workspace],
        "workspace": workspace,
    }


def me_response() -> dict:
    base = auth_response()
    return {
        "user": base["user"],
        "organization": base["organization"],
        "active_project": base["active_project"],
        "projects": base["projects"],
        "workspace": base["workspace"],
    }


def profile_response() -> dict:
    return {
        "full_name": "SDK User",
        "email": "dev@pinbridge.io",
        "workspace_name": "SDK Workspace",
        "company_name": "PinBridge",
        "company_website": "https://pinbridge.io",
        "billing_email": "billing@pinbridge.io",
        "billing_phone": "+1-555-0100",
        "tax_id": None,
        "address_line1": None,
        "address_line2": None,
        "address_city": None,
        "address_state": None,
        "address_postal_code": None,
        "address_country": None,
    }


def updated_profile_response() -> dict:
    payload = profile_response()
    payload["workspace_name"] = "SDK Workspace Updated"
    payload["company_name"] = "PinBridge SDK"
    return payload


def pinterest_account_response() -> dict:
    return {
        "id": UUID4,
        "workspace_id": UUID2,
        "pinterest_user_id": "pin-user-id",
        "display_name": "SDK Pinterest",
        "username": "sdk-pin",
        "scopes": "boards:read,boards:write,pins:read,pins:write",
        "created_at": TS,
        "updated_at": TS,
        "revoked_at": None,
    }


def board_response() -> dict:
    return {
        "id": "123-board",
        "name": "SDK Board",
        "description": "Board from tests",
        "privacy": "PUBLIC",
    }


def pin_response() -> dict:
    return {
        "id": UUID1,
        "workspace_id": UUID2,
        "pinterest_account_id": UUID4,
        "status": "queued",
        "media_type": "image",
        "title": "A Pin",
        "description": "Pin description",
        "link_url": "https://example.com",
        "media_url": "https://example.com/image.jpg",
        "image_url": "https://example.com/image.jpg",
        "asset_id": UUID3,
        "board_id": "123-board",
        "pinterest_pin_id": None,
        "error_code": None,
        "error_message": None,
        "idempotency_key": "idem-123",
        "created_at": TS,
        "updated_at": TS,
        "published_at": None,
    }


def job_status_response() -> dict:
    return {
        "job_id": UUID1,
        "pin_id": UUID1,
        "status": "queued",
        "submitted_at": TS,
        "completed_at": None,
        "pinterest_pin_id": None,
        "error_code": None,
        "error_message": None,
    }


def import_job_response(*, job_id: str, source_type: str) -> dict:
    return {
        "id": job_id,
        "workspace_id": UUID2,
        "source_type": source_type,
        "status": "processing",
        "source_filename": "pins.csv" if source_type == "csv" else None,
        "total_rows": 1,
        "processed_rows": 1,
        "created_rows": 1,
        "existing_rows": 0,
        "failed_rows": 0,
        "results": [
            {
                "row_number": 1,
                "status": "created",
                "pin_id": UUID1,
                "schedule_id": None,
                "idempotency_key": "idem-import-1",
                "error_code": None,
                "error_message": None,
            }
        ],
        "error_message": None,
        "started_at": TS,
        "completed_at": None,
        "created_at": TS,
        "updated_at": TS,
    }


def schedule_response() -> dict:
    return {
        "id": UUID3,
        "workspace_id": UUID2,
        "pinterest_account_id": UUID4,
        "run_at": "2026-02-24T12:00:00Z",
        "status": "scheduled",
        "payload": {
            "board_id": "123-board",
            "title": "Scheduled pin",
            "description": "Scheduled",
            "link_url": "https://example.com",
            "media_type": "image",
            "media_url": "https://example.com/image.jpg",
            "image_url": "https://example.com/image.jpg",
            "asset_id": UUID3,
        },
        "last_error": None,
        "pin_id": None,
        "created_at": TS,
        "updated_at": TS,
    }


def webhook_response() -> dict:
    return {
        "id": UUID3,
        "workspace_id": UUID2,
        "url": "https://example.com/hook",
        "events": ["pin.published", "pin.failed"],
        "is_enabled": True,
        "created_at": TS,
        "updated_at": TS,
    }


def api_key_response() -> dict:
    return {
        "id": UUID3,
        "workspace_id": UUID2,
        "name": "default",
        "created_at": TS,
        "revoked_at": None,
    }


def api_key_create_response() -> dict:
    payload = api_key_response()
    payload["api_key"] = "pb_live_123"
    return payload


def projects_context_response() -> dict:
    workspace = {
        "id": UUID2,
        "name": "SDK Workspace",
        "environment": "production",
        "plan": "starter",
        "created_at": TS,
    }
    sandbox = {
        "id": UUID4,
        "name": "SDK Sandbox",
        "environment": "sandbox",
        "plan": "free",
        "created_at": TS,
    }
    return {
        "organization": {"id": UUID3, "name": "SDK Org"},
        "active_project": workspace,
        "projects": [workspace, sandbox],
    }


def project_switch_response() -> dict:
    payload = projects_context_response()
    payload["active_project"] = payload["projects"][1]
    payload["access_token"] = "jwt-switched-token"
    payload["token_type"] = "bearer"
    payload["expires_in"] = 3600
    return payload


def pricing_catalog_response() -> dict:
    return {
        "source": "cache",
        "refreshed_at": TS,
        "plans": [
            {
                "plan": "starter",
                "name": "Starter",
                "subtitle": "For small teams",
                "highlight": False,
                "feature_bullets": ["1000 API calls"],
                "monthly_overage": None,
                "quota_calls_monthly": 1000,
                "pinterest_accounts_limit": 2,
                "uploaded_media_assets": True,
                "bulk_imports": True,
                "activity_log_retention_days": 30,
                "overage_billing_threshold_pins": 100,
                "monthly_price": {
                    "billing_cycle": "monthly",
                    "unit_amount": 1900,
                    "currency": "usd",
                    "amount_display": "$19",
                },
                "annual_price": {
                    "billing_cycle": "annual",
                    "unit_amount": 19000,
                    "currency": "usd",
                    "amount_display": "$190",
                },
            }
        ],
    }


def billing_status_response() -> dict:
    return {
        "plan": "starter",
        "billing_cycle": "monthly",
        "billing_status": "active",
        "current_period_start": TS,
        "current_period_end": TS,
        "subscription_cancel_at": None,
        "quota_calls_monthly": 1000,
        "calls_used": 10,
        "overage_pins_used": 0,
        "quota_reset_at": TS,
        "pinterest_accounts_limit": 2,
        "uploaded_media_assets": True,
        "bulk_imports": True,
        "overage_billing_threshold_pins": 100,
    }


def rate_meter_response() -> dict:
    return {
        "account": {
            "account_id": UUID4,
            "tokens_available": 40,
            "capacity": 50,
            "refill_rate": 5,
        },
        "global": {
            "tokens_available": 1000,
            "capacity": 1200,
            "refill_rate": 20,
        },
    }


def asset_response() -> dict:
    return {
        "id": UUID3,
        "workspace_id": UUID2,
        "asset_type": "image",
        "original_filename": "pin.png",
        "stored_filename": f"{UUID3}.png",
        "content_type": "image/png",
        "file_size_bytes": 68,
        "public_url": f"https://api.pinbridge.test/v1/assets/{UUID3}/content",
        "created_at": TS,
        "updated_at": TS,
    }


def asset_list_response() -> dict:
    return {
        "assets": [asset_response()],
        "total": 1,
        "storage_used_bytes": 68,
        "storage_quota_bytes": 10_000,
        "storage_used_percent": 1,
    }


def asset_delete_response() -> dict:
    return {
        "deleted": True,
        "requires_confirmation": False,
        "referenced_pin_count": 0,
        "freed_bytes": 68,
    }


def bulk_asset_delete_response() -> dict:
    return {
        "deleted": [UUID3],
        "requires_confirmation": [],
        "total_freed_bytes": 68,
        "deleted_items": [
            {
                "asset_id": UUID3,
                "workspace_id": UUID2,
                "original_filename": "pin.png",
                "file_size_bytes": 68,
                "referenced_pin_count": 0,
                "freed_bytes": 68,
            }
        ],
        "requires_confirmation_items": [],
    }


def bulk_operation_response() -> dict:
    return {
        "succeeded_count": 1,
        "skipped_count": 0,
        "failed_count": 0,
        "results": [{"id": UUID1, "status": "succeeded"}],
    }


def team_member_response() -> dict:
    return {
        "id": UUID1,
        "organization_id": UUID3,
        "user_id": UUID1,
        "role": "admin",
        "invited_by_user_id": None,
        "accepted_at": TS,
        "created_at": TS,
        "updated_at": TS,
        "user": auth_user_response(),
        "invited_by": None,
    }


def team_members_list_response() -> dict:
    return {"items": [team_member_response()]}


def team_invitation_response() -> dict:
    return {
        "id": UUID4,
        "organization_id": UUID3,
        "email": "teammate@pinbridge.io",
        "role": "editor",
        "invited_by_user_id": UUID1,
        "expires_at": TS,
        "accepted_at": None,
        "revoked_at": None,
        "created_at": TS,
        "updated_at": TS,
        "inviter_name": "SDK User",
        "inviter_email": "dev@pinbridge.io",
    }


def team_invitations_list_response() -> dict:
    return {"items": [team_invitation_response()]}


def team_action_response() -> dict:
    return {"message": "Done"}


def mcp_quota_response() -> dict:
    return {
        "week": "2026-W09",
        "requests_used": 12,
        "requests_limit": 100,
        "quota_exhausted": False,
        "resets_at": "2026-03-02T00:00:00Z",
    }


def email_preferences_response() -> dict:
    return {
        "id": UUID1,
        "workspace_id": UUID2,
        "user_id": UUID1,
        "transactional_enabled": True,
        "alerts_enabled": False,
        "verification_enabled": True,
        "created_at": TS,
        "updated_at": TS,
    }


def build_transport() -> httpx.MockTransport:
    def handler(request: httpx.Request) -> httpx.Response:
        path = request.url.path
        method = request.method

        if method == "GET" and path == "/":
            return httpx.Response(200, json=root_response())
        if method == "GET" and path == "/healthz":
            return httpx.Response(200, json=health_response())
        if method == "GET" and path == "/readyz":
            return httpx.Response(200, json=readiness_response())
        if method == "POST" and path == "/v1/stripe/webhook":
            return httpx.Response(200, json={"status": "accepted"})

        if method == "POST" and path == "/v1/auth/register":
            return httpx.Response(200, json=auth_response())
        if method == "POST" and path == "/v1/auth/login":
            return httpx.Response(200, json=auth_response())
        if method == "POST" and path == "/v1/auth/forgot-password":
            return httpx.Response(200, json={"message": "Password reset email sent"})
        if method == "POST" and path == "/v1/auth/reset-password":
            return httpx.Response(200, json={"message": "Password reset complete"})
        if method == "POST" and path == "/v1/auth/change-password":
            return httpx.Response(200, json={"message": "Password changed"})
        if method == "POST" and path == "/v1/auth/email/verify/request":
            return httpx.Response(200, json={"message": "Verification email sent"})
        if method == "GET" and path == "/v1/auth/email/verify":
            return httpx.Response(200, json={"message": "Email verified"})
        if method == "GET" and path == "/v1/auth/me":
            return httpx.Response(200, json=me_response())
        if method == "GET" and path == "/v1/auth/profile":
            return httpx.Response(200, json=profile_response())
        if method == "PUT" and path == "/v1/auth/profile":
            return httpx.Response(200, json=updated_profile_response())

        if method == "GET" and path == "/v1/pinterest/oauth/start":
            return httpx.Response(
                200, json={"authorization_url": "https://pinterest.com/oauth/demo"}
            )
        if method == "GET" and path == "/v1/pinterest/oauth/callback":
            return httpx.Response(
                200,
                json={"status": "connected", "message": "Account linked", "account_id": UUID4},
            )
        if method == "GET" and path == "/v1/pinterest/accounts":
            return httpx.Response(200, json=[pinterest_account_response()])
        if method == "DELETE" and path == f"/v1/pinterest/accounts/{UUID4}":
            return httpx.Response(204)
        if method == "GET" and path == "/v1/pinterest/boards":
            return httpx.Response(200, json=[board_response()])
        if method == "POST" and path == "/v1/pinterest/boards":
            return httpx.Response(200, json=board_response())
        if method == "DELETE" and path == "/v1/pinterest/boards/123-board":
            return httpx.Response(204)

        if method == "POST" and path in {"/v1/assets/images", "/v1/assets/videos"}:
            return httpx.Response(200, json=asset_response())
        if method == "GET" and path == f"/v1/assets/{UUID3}":
            return httpx.Response(200, json=asset_response())
        if method == "GET" and path == f"/v1/assets/{UUID3}/content":
            return httpx.Response(200, content=b"\x89PNG\r\n\x1a\nmock-content")
        if method == "GET" and path == "/v1/assets":
            return httpx.Response(200, json=asset_list_response())
        if method == "DELETE" and path == f"/v1/assets/{UUID3}":
            return httpx.Response(200, json=asset_delete_response())
        if method == "DELETE" and path == "/v1/assets":
            return httpx.Response(200, json=bulk_asset_delete_response())

        if method == "POST" and path == "/v1/pins":
            return httpx.Response(200, json=pin_response())
        if method == "GET" and path == f"/v1/pins/{UUID1}":
            return httpx.Response(200, json=pin_response())
        if method == "GET" and path == "/v1/pins":
            return httpx.Response(200, json=[pin_response()])
        if method == "DELETE" and path == f"/v1/pins/{UUID1}":
            return httpx.Response(204)
        if method == "POST" and path == f"/v1/pins/{UUID1}/retry":
            return httpx.Response(200, json=pin_response())
        if method == "POST" and path in {"/v1/pins/bulk-delete", "/v1/pins/bulk-retry"}:
            return httpx.Response(200, json=bulk_operation_response())

        if method == "POST" and path == "/v1/pins/imports/json":
            return httpx.Response(200, json=import_job_response(job_id=UUID5, source_type="json"))
        if method == "POST" and path == "/v1/pins/imports/csv":
            return httpx.Response(200, json=import_job_response(job_id=UUID6, source_type="csv"))
        if method == "GET" and path == f"/v1/pins/imports/{UUID5}":
            return httpx.Response(200, json=import_job_response(job_id=UUID5, source_type="json"))
        if method == "GET" and path == f"/v1/pins/imports/{UUID6}":
            return httpx.Response(200, json=import_job_response(job_id=UUID6, source_type="csv"))
        if method == "GET" and path == "/v1/pins/imports":
            return httpx.Response(
                200,
                json=[
                    import_job_response(job_id=UUID6, source_type="csv"),
                    import_job_response(job_id=UUID5, source_type="json"),
                ],
            )

        if method == "GET" and path == f"/v1/jobs/{UUID1}":
            return httpx.Response(200, json=job_status_response())

        if method == "POST" and path == "/v1/schedules":
            return httpx.Response(200, json=schedule_response())
        if method == "GET" and path == f"/v1/schedules/{UUID3}":
            return httpx.Response(200, json=schedule_response())
        if method == "GET" and path == "/v1/schedules":
            return httpx.Response(200, json=[schedule_response()])
        if method == "POST" and path == f"/v1/schedules/{UUID3}/cancel":
            payload = schedule_response()
            payload["status"] = "canceled"
            return httpx.Response(200, json=payload)
        if method == "POST" and path == f"/v1/schedules/{UUID3}/retry":
            payload = schedule_response()
            payload["status"] = "queued"
            return httpx.Response(200, json=payload)
        if method == "DELETE" and path == f"/v1/schedules/{UUID3}":
            return httpx.Response(204)
        if method == "POST" and path in {
            "/v1/schedules/bulk-cancel",
            "/v1/schedules/bulk-retry",
            "/v1/schedules/bulk-delete",
        }:
            return httpx.Response(200, json=bulk_operation_response())

        if method == "POST" and path == "/v1/webhooks":
            return httpx.Response(200, json=webhook_response())
        if method == "PATCH" and path == f"/v1/webhooks/{UUID3}":
            payload = webhook_response()
            payload["is_enabled"] = False
            return httpx.Response(200, json=payload)
        if method == "GET" and path == f"/v1/webhooks/{UUID3}":
            return httpx.Response(200, json=webhook_response())
        if method == "GET" and path == "/v1/webhooks":
            return httpx.Response(200, json=[webhook_response()])
        if method == "DELETE" and path == f"/v1/webhooks/{UUID3}":
            return httpx.Response(204)

        if method == "POST" and path == "/v1/api-keys":
            return httpx.Response(200, json=api_key_create_response())
        if method == "GET" and path == "/v1/api-keys":
            return httpx.Response(200, json=[api_key_response()])
        if method == "PATCH" and path == f"/v1/api-keys/{UUID3}":
            payload = api_key_response()
            payload["name"] = "rotated"
            return httpx.Response(200, json=payload)
        if method == "DELETE" and path == f"/v1/api-keys/{UUID3}":
            return httpx.Response(204)

        if method == "GET" and path == "/v1/projects":
            return httpx.Response(200, json=projects_context_response())
        if method == "POST" and path == "/v1/projects/sandbox":
            return httpx.Response(200, json=projects_context_response())
        if method == "POST" and path == "/v1/projects/switch":
            return httpx.Response(200, json=project_switch_response())
        if method == "POST" and path == "/v1/projects/sandbox/reset":
            return httpx.Response(200, json=projects_context_response())

        if method == "GET" and path == "/v1/billing/pricing":
            return httpx.Response(200, json=pricing_catalog_response())
        if method == "GET" and path == "/v1/billing/status":
            return httpx.Response(200, json=billing_status_response())
        if method == "POST" and path == "/v1/billing/checkout":
            return httpx.Response(200, json={"url": "https://billing.example.com/checkout"})
        if method == "POST" and path == "/v1/billing/portal":
            return httpx.Response(200, json={"url": "https://billing.example.com/portal"})

        if method == "GET" and path == "/v1/rate-meter":
            return httpx.Response(200, json=rate_meter_response())

        if method == "GET" and path == "/v1/team/members":
            return httpx.Response(200, json=team_members_list_response())
        if method == "GET" and path == "/v1/team/invitations":
            return httpx.Response(200, json=team_invitations_list_response())
        if method == "POST" and path == "/v1/team/invitations":
            return httpx.Response(201, json=team_invitation_response())
        if method == "POST" and path == f"/v1/team/invitations/{UUID4}/resend":
            return httpx.Response(200, json=team_invitation_response())
        if method == "DELETE" and path == f"/v1/team/invitations/{UUID4}":
            return httpx.Response(200, json=team_action_response())
        if method == "PATCH" and path == f"/v1/team/members/{UUID1}":
            return httpx.Response(200, json=team_member_response())

        if method == "GET" and path == "/v1/mcp/quota":
            return httpx.Response(200, json=mcp_quota_response())
        if method == "POST" and path == "/v1/mcp/track":
            return httpx.Response(200, json=mcp_quota_response())

        if method == "GET" and path == "/v1/email/preferences":
            return httpx.Response(200, json=email_preferences_response())
        if method == "PATCH" and path == "/v1/email/preferences":
            payload = email_preferences_response()
            payload["alerts_enabled"] = True
            return httpx.Response(200, json=payload)

        raise AssertionError(f"Unhandled request: {method} {path}")

    return httpx.MockTransport(handler)


def import_example(name: str):
    return importlib.import_module(name)


def patch_sync_client(monkeypatch, module, *, transport: httpx.MockTransport) -> None:
    from pinbridge_sdk import PinbridgeClient

    def factory(*, require_api_key: bool = False):
        return PinbridgeClient(
            base_url="https://api.pinbridge.test",
            api_key="pb_test" if require_api_key else None,
            transport=transport,
        )

    monkeypatch.setattr(module, "make_sync_client", factory)


def patch_async_client(monkeypatch, module, *, transport: httpx.MockTransport) -> None:
    from pinbridge_sdk import AsyncPinbridgeClient

    def factory(*, require_api_key: bool = False):
        return AsyncPinbridgeClient(
            base_url="https://api.pinbridge.test",
            api_key="pb_test" if require_api_key else None,
            transport=transport,
        )

    monkeypatch.setattr(module, "make_async_client", factory)


def test_health_root(monkeypatch, capsys):
    module = import_example("health_root")
    patch_sync_client(monkeypatch, module, transport=build_transport())
    assert module.main() == 0
    output = capsys.readouterr().out
    assert "Health: status=ok" in output
    assert "Readiness: status=ok" in output


def test_system_readiness_and_webhooks(monkeypatch, capsys):
    module = import_example("system_readiness_and_webhooks")
    patch_sync_client(monkeypatch, module, transport=build_transport())
    monkeypatch.setenv("PINBRIDGE_FORWARD_STRIPE_WEBHOOK", "1")
    monkeypatch.setenv("PINBRIDGE_STRIPE_SIGNATURE", "t=1,v1=abc123")
    monkeypatch.setenv("PINBRIDGE_STRIPE_WEBHOOK_BODY", '{"type":"invoice.paid"}')
    assert module.main() == 0
    output = capsys.readouterr().out
    assert "Readiness: status=ok" in output
    assert "Stripe webhook forwarded: accepted" in output


def test_auth_and_profile(monkeypatch, capsys):
    module = import_example("auth_and_profile")
    patch_sync_client(monkeypatch, module, transport=build_transport())
    monkeypatch.setenv("PINBRIDGE_EMAIL", "dev@pinbridge.io")
    monkeypatch.setenv("PINBRIDGE_PASSWORD", "super-secret-123")
    assert module.main() == 0
    assert "Authenticated as: dev@pinbridge.io" in capsys.readouterr().out


def test_auth_full_lifecycle(monkeypatch, capsys):
    module = import_example("auth_full_lifecycle")
    patch_sync_client(monkeypatch, module, transport=build_transport())

    monkeypatch.setenv("PINBRIDGE_REGISTER_USER", "1")
    monkeypatch.setenv("PINBRIDGE_REGISTER_FULL_NAME", "SDK User")
    monkeypatch.setenv("PINBRIDGE_REGISTER_EMAIL", "dev@pinbridge.io")
    monkeypatch.setenv("PINBRIDGE_REGISTER_PASSWORD", "super-secret-123")

    monkeypatch.setenv("PINBRIDGE_UPDATE_PROFILE", "1")
    monkeypatch.setenv("PINBRIDGE_REQUEST_EMAIL_VERIFICATION", "1")
    monkeypatch.setenv("PINBRIDGE_EMAIL_VERIFICATION_TOKEN", "verify-token")
    monkeypatch.setenv("PINBRIDGE_REQUEST_PASSWORD_RESET", "1")
    monkeypatch.setenv("PINBRIDGE_PASSWORD_RESET_TOKEN", "tok_1234567890123456789012")
    monkeypatch.setenv("PINBRIDGE_NEW_PASSWORD", "new-password-123")
    monkeypatch.setenv("PINBRIDGE_CHANGE_PASSWORD", "1")
    monkeypatch.setenv("PINBRIDGE_CURRENT_PASSWORD", "super-secret-123")
    monkeypatch.setenv("PINBRIDGE_NEXT_PASSWORD", "super-secret-456")

    assert module.main() == 0
    output = capsys.readouterr().out
    assert "Registered new user:" in output
    assert "Profile updated for workspace:" in output
    assert "Email verification result:" in output
    assert "Password reset result:" in output
    assert "Password change result:" in output


def test_api_keys_lifecycle(monkeypatch, capsys):
    module = import_example("api_keys_lifecycle")
    patch_sync_client(monkeypatch, module, transport=build_transport())
    monkeypatch.setenv("PINBRIDGE_EMAIL", "dev@pinbridge.io")
    monkeypatch.setenv("PINBRIDGE_PASSWORD", "super-secret-123")
    assert module.main() == 0
    output = capsys.readouterr().out
    assert "Created API key id=" in output
    assert "Revoked the example key" in output


def test_projects_sandbox(monkeypatch, capsys):
    module = import_example("projects_sandbox")
    patch_sync_client(monkeypatch, module, transport=build_transport())
    monkeypatch.setenv("PINBRIDGE_EMAIL", "dev@pinbridge.io")
    monkeypatch.setenv("PINBRIDGE_PASSWORD", "super-secret-123")
    monkeypatch.setenv("PINBRIDGE_RESET_SANDBOX", "1")
    assert module.main() == 0
    assert "Switched active project to sandbox" in capsys.readouterr().out


def test_pinterest_oauth_callback_and_disconnect(monkeypatch, capsys):
    module = import_example("pinterest_oauth_callback_and_disconnect")
    patch_sync_client(monkeypatch, module, transport=build_transport())
    monkeypatch.setenv("PINBRIDGE_EMAIL", "dev@pinbridge.io")
    monkeypatch.setenv("PINBRIDGE_PASSWORD", "super-secret-123")
    monkeypatch.setenv("PINBRIDGE_OAUTH_CODE", "oauth-code")
    monkeypatch.setenv("PINBRIDGE_OAUTH_STATE", "oauth-state")
    monkeypatch.setenv("PINBRIDGE_REVOKE_FIRST_ACCOUNT", "1")
    assert module.main() == 0
    output = capsys.readouterr().out
    assert "OAuth callback result: connected" in output
    assert "Revoked account:" in output


def test_publish_from_image_url(monkeypatch, capsys):
    module = import_example("publish_from_image_url")
    patch_sync_client(monkeypatch, module, transport=build_transport())
    monkeypatch.setenv("PINBRIDGE_API_KEY", "pb_test")
    monkeypatch.setenv("PINBRIDGE_PIN_TITLE", "Spring drop")
    monkeypatch.setenv("PINBRIDGE_IMAGE_URL", "https://example.com/image.jpg")
    assert module.main() == 0
    assert "Pin queued: id=" in capsys.readouterr().out


def test_upload_and_publish_local_media(monkeypatch, tmp_path, capsys):
    module = import_example("upload_and_publish_local_media")
    patch_sync_client(monkeypatch, module, transport=build_transport())
    image_path = tmp_path / "pin.png"
    image_path.write_bytes(b"\x89PNG\r\n\x1a\n")
    monkeypatch.setenv("PINBRIDGE_API_KEY", "pb_test")
    monkeypatch.setenv("PINBRIDGE_IMAGE_PATH", str(image_path))
    assert module.main() == 0
    assert "Media source: uploaded image pin.png" in capsys.readouterr().out


def test_assets_retrieve_and_download(monkeypatch, tmp_path, capsys):
    module = import_example("assets_retrieve_and_download")
    patch_sync_client(monkeypatch, module, transport=build_transport())

    image_path = tmp_path / "pin.png"
    output_path = tmp_path / "downloaded.bin"
    image_path.write_bytes(b"\x89PNG\r\n\x1a\n")

    monkeypatch.setenv("PINBRIDGE_API_KEY", "pb_test")
    monkeypatch.setenv("PINBRIDGE_IMAGE_PATH", str(image_path))
    monkeypatch.setenv("PINBRIDGE_ASSET_OUTPUT_PATH", str(output_path))

    assert module.main() == 0
    output = capsys.readouterr().out
    assert "Asset id:" in output
    assert "Downloaded bytes:" in output
    assert output_path.exists()
    assert output_path.read_bytes() == b"\x89PNG\r\n\x1a\nmock-content"


def test_pins_bulk_import_and_management(monkeypatch, capsys):
    module = import_example("pins_bulk_import_and_management")
    patch_sync_client(monkeypatch, module, transport=build_transport())

    monkeypatch.setenv("PINBRIDGE_API_KEY", "pb_test")
    monkeypatch.setenv("PINBRIDGE_IMAGE_URL", "https://example.com/image.jpg")
    monkeypatch.setenv("PINBRIDGE_DELETE_CREATED_PIN", "1")

    assert module.main() == 0
    output = capsys.readouterr().out
    assert "Created pin:" in output
    assert "JSON import job:" in output
    assert "CSV import job:" in output
    assert "Deleted the created pin" in output


def test_schedules_lifecycle(monkeypatch, capsys):
    module = import_example("schedules_lifecycle")
    patch_sync_client(monkeypatch, module, transport=build_transport())
    monkeypatch.setenv("PINBRIDGE_API_KEY", "pb_test")
    monkeypatch.setenv("PINBRIDGE_IMAGE_URL", "https://example.com/image.jpg")
    monkeypatch.setenv("PINBRIDGE_CANCEL_SCHEDULE", "1")
    assert module.main() == 0
    assert "Cancel step: canceled" in capsys.readouterr().out


def test_webhooks_lifecycle(monkeypatch, capsys):
    module = import_example("webhooks_lifecycle")
    patch_sync_client(monkeypatch, module, transport=build_transport())
    monkeypatch.setenv("PINBRIDGE_API_KEY", "pb_test")
    monkeypatch.setenv("PINBRIDGE_WEBHOOK_URL", "https://example.com/hook")
    monkeypatch.setenv("PINBRIDGE_WEBHOOK_SECRET", "0123456789012345")
    assert module.main() == 0
    assert "Deleted the example webhook" in capsys.readouterr().out


def test_billing_and_rate_meter(monkeypatch, capsys):
    module = import_example("billing_and_rate_meter")
    patch_sync_client(monkeypatch, module, transport=build_transport())
    monkeypatch.setenv("PINBRIDGE_EMAIL", "dev@pinbridge.io")
    monkeypatch.setenv("PINBRIDGE_PASSWORD", "super-secret-123")
    monkeypatch.setenv("PINBRIDGE_CREATE_PORTAL", "1")
    assert module.main() == 0
    output = capsys.readouterr().out
    assert "Current plan: starter" in output
    assert "Customer portal URL:" in output


def test_billing_checkout_flow(monkeypatch, capsys):
    module = import_example("billing_checkout_flow")
    patch_sync_client(monkeypatch, module, transport=build_transport())
    monkeypatch.setenv("PINBRIDGE_EMAIL", "dev@pinbridge.io")
    monkeypatch.setenv("PINBRIDGE_PASSWORD", "super-secret-123")
    monkeypatch.setenv("PINBRIDGE_CHECKOUT_PLAN", "growth")
    monkeypatch.setenv("PINBRIDGE_CHECKOUT_CYCLE", "annual")
    assert module.main() == 0
    output = capsys.readouterr().out
    assert "Requested checkout: plan=growth cycle=annual" in output
    assert "Checkout URL:" in output


def test_async_publish_workflow(monkeypatch, capsys):
    module = import_example("async_publish_workflow")
    patch_async_client(monkeypatch, module, transport=build_transport())
    monkeypatch.setenv("PINBRIDGE_API_KEY", "pb_test")
    monkeypatch.setenv("PINBRIDGE_IMAGE_URL", "https://example.com/image.jpg")
    assert asyncio.run(module.main()) == 0
    assert "Async schedule id:" in capsys.readouterr().out


def test_advanced_client_patterns(monkeypatch, capsys):
    module = import_example("advanced_client_patterns")
    patch_sync_client(monkeypatch, module, transport=build_transport())
    monkeypatch.setenv("PINBRIDGE_API_KEY", "pb_test")
    assert module.main() == 0
    output = capsys.readouterr().out
    assert "Derived client health: ok" in output
    assert "Custom resource ping: ok" in output


def test_webhook_signature_verification(monkeypatch, capsys):
    module = import_example("webhook_signature_verification")
    monkeypatch.setenv("PINBRIDGE_WEBHOOK_SECRET", "0123456789012345")
    monkeypatch.setenv("PINBRIDGE_WEBHOOK_BODY", '{"pin_id":"demo"}')
    signature = module.compute_webhook_signature(b'{"pin_id":"demo"}', "0123456789012345")
    monkeypatch.setenv("PINBRIDGE_WEBHOOK_SIGNATURE", signature)
    assert module.main() == 0
    assert "Provided signature valid: True" in capsys.readouterr().out


def test_webhook_receiver_verification():
    module = import_example("webhook_receiver")
    payload = b'{"pin_id":"demo"}'
    signature_module = import_example("webhook_signature_verification")
    signature = signature_module.compute_webhook_signature(payload, "0123456789012345")
    is_valid, details = module.verify_delivery(
        {
            "X-PinBridge-Signature": signature,
            "X-PinBridge-Event": "pin.published",
            "X-PinBridge-Delivery-ID": "delivery-123",
        },
        payload,
        secret="0123456789012345",
    )
    assert is_valid is True
    assert details["event"] == "pin.published"
    assert details["payload"]["pin_id"] == "demo"


def test_recipe_shopify_product_publish(monkeypatch, capsys):
    module = import_example("recipe_shopify_product_publish")
    patch_sync_client(monkeypatch, module, transport=build_transport())
    monkeypatch.setenv("PINBRIDGE_API_KEY", "pb_test")
    monkeypatch.setenv("SHOPIFY_PRODUCT_URL", "https://shop.example.com/products/demo")
    monkeypatch.setenv("SHOPIFY_IMAGE_URL", "https://cdn.example.com/demo.jpg")
    assert module.main() == 0
    assert "Published Shopify product pin:" in capsys.readouterr().out


def test_recipe_cms_scheduled_pin(monkeypatch, capsys):
    module = import_example("recipe_cms_scheduled_pin")
    patch_sync_client(monkeypatch, module, transport=build_transport())
    monkeypatch.setenv("PINBRIDGE_API_KEY", "pb_test")
    monkeypatch.setenv("CMS_ARTICLE_URL", "https://cms.example.com/articles/demo")
    monkeypatch.setenv("CMS_IMAGE_URL", "https://cdn.example.com/demo.jpg")
    assert module.main() == 0
    assert "Scheduled CMS article" in capsys.readouterr().out


def test_recipe_multi_account_campaign(monkeypatch, capsys):
    module = import_example("recipe_multi_account_campaign")
    patch_sync_client(monkeypatch, module, transport=build_transport())
    monkeypatch.setenv("PINBRIDGE_API_KEY", "pb_test")
    monkeypatch.setenv("PINBRIDGE_IMAGE_URL", "https://cdn.example.com/demo.jpg")
    assert module.main() == 0
    assert "Fan-out complete across 1 account(s)" in capsys.readouterr().out


def test_assets_manage_and_cleanup(monkeypatch, capsys):
    module = import_example("assets_manage_and_cleanup")
    patch_sync_client(monkeypatch, module, transport=build_transport())
    monkeypatch.setenv("PINBRIDGE_API_KEY", "pb_test")
    monkeypatch.setenv("PINBRIDGE_DELETE_ASSETS", "1")
    assert module.main() == 0
    output = capsys.readouterr().out
    assert "Assets: 1 of 1" in output
    assert "Deleted asset: deleted=True" in output
    assert "Bulk delete: deleted=1" in output


def test_pins_retry_and_bulk_ops(monkeypatch, capsys):
    module = import_example("pins_retry_and_bulk_ops")
    patch_sync_client(monkeypatch, module, transport=build_transport())
    monkeypatch.setenv("PINBRIDGE_API_KEY", "pb_test")
    monkeypatch.setenv("PINBRIDGE_DELETE_PINS", "1")
    assert module.main() == 0
    output = capsys.readouterr().out
    assert "Retried pin:" in output
    assert "Bulk retry: succeeded=1" in output
    assert "Bulk delete: succeeded=1" in output


def test_schedules_bulk_management(monkeypatch, capsys):
    module = import_example("schedules_bulk_management")
    patch_sync_client(monkeypatch, module, transport=build_transport())
    monkeypatch.setenv("PINBRIDGE_API_KEY", "pb_test")
    monkeypatch.setenv("PINBRIDGE_MUTATE_SCHEDULES", "1")
    assert module.main() == 0
    output = capsys.readouterr().out
    assert "Retried schedule:" in output
    assert "Bulk cancel: succeeded=1" in output
    assert "Deleted schedule:" in output


def test_team_members_and_invitations(monkeypatch, capsys):
    module = import_example("team_members_and_invitations")
    patch_sync_client(monkeypatch, module, transport=build_transport())
    monkeypatch.setenv("PINBRIDGE_EMAIL", "dev@pinbridge.io")
    monkeypatch.setenv("PINBRIDGE_PASSWORD", "super-secret-123")
    monkeypatch.setenv("PINBRIDGE_MANAGE_TEAM", "1")
    assert module.main() == 0
    output = capsys.readouterr().out
    assert "Team members: 1" in output
    assert "Created invitation:" in output
    assert "Revoked invitation:" in output


def test_email_preferences(monkeypatch, capsys):
    module = import_example("email_preferences")
    patch_sync_client(monkeypatch, module, transport=build_transport())
    monkeypatch.setenv("PINBRIDGE_EMAIL", "dev@pinbridge.io")
    monkeypatch.setenv("PINBRIDGE_PASSWORD", "super-secret-123")
    monkeypatch.setenv("PINBRIDGE_UPDATE_EMAIL_PREFERENCES", "1")
    assert module.main() == 0
    output = capsys.readouterr().out
    assert "Current preferences:" in output
    assert "Updated preferences:" in output


def test_mcp_quota_and_track(monkeypatch, capsys):
    module = import_example("mcp_quota_and_track")
    patch_sync_client(monkeypatch, module, transport=build_transport())
    monkeypatch.setenv("PINBRIDGE_API_KEY", "pb_test")
    monkeypatch.setenv("PINBRIDGE_TRACK_MCP", "1")
    assert module.main() == 0
    output = capsys.readouterr().out
    assert "MCP quota (2026-W09):" in output
    assert "After track:" in output
