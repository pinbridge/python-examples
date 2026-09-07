"""Contract guard: the smoke-test response fixtures must satisfy the SDK models.

The example smoke tests drive each script through an ``httpx.MockTransport`` whose
response bodies are hand-written fixtures. Those fixtures can silently drift from the
shapes the SDK (and therefore the API it tracks) actually returns. This test parses
every fixture with the matching SDK Pydantic model, so a missing/renamed field or a
changed type fails CI instead of producing a misleadingly-green mock run.

It is not a substitute for testing against a live API, but it does catch drift between
the examples' fixtures and the installed SDK's models.
"""

from __future__ import annotations

import test_examples_smoke as smoke

from pinbridge_sdk.models import (
    APIKeyCreateResponse,
    APIKeyResponse,
    AssetDeleteResponse,
    AssetListResponse,
    AssetResponse,
    AuthResponse,
    BillingStatusResponse,
    BoardResponse,
    BulkAssetDeleteResponse,
    BulkOperationResponse,
    EmailPreferencesResponse,
    HealthResponse,
    ImportJobResponse,
    JobStatusResponse,
    MCPQuotaResponse,
    MeResponse,
    PinResponse,
    PinterestAccountResponse,
    PricingCatalogResponse,
    ProfileResponse,
    ProjectsContextResponse,
    ProjectSwitchResponse,
    RateMeterResponse,
    ReadinessResponse,
    RootResponse,
    ScheduleResponse,
    TeamInvitationResponse,
    TeamInvitationsListResponse,
    TeamMemberResponse,
    TeamMembersListResponse,
    WebhookResponse,
)

import pytest

# (SDK model, fixture payload) pairs. Every fixture the smoke transport returns should
# be represented here so a drift in any one of them is caught.
CASES = [
    (RootResponse, smoke.root_response()),
    (HealthResponse, smoke.health_response()),
    (ReadinessResponse, smoke.readiness_response()),
    (AuthResponse, smoke.auth_response()),
    (MeResponse, smoke.me_response()),
    (ProfileResponse, smoke.profile_response()),
    (ProfileResponse, smoke.updated_profile_response()),
    (PinterestAccountResponse, smoke.pinterest_account_response()),
    (BoardResponse, smoke.board_response()),
    (PinResponse, smoke.pin_response()),
    (JobStatusResponse, smoke.job_status_response()),
    (ImportJobResponse, smoke.import_job_response(job_id=smoke.UUID5, source_type="json")),
    (ImportJobResponse, smoke.import_job_response(job_id=smoke.UUID6, source_type="csv")),
    (ScheduleResponse, smoke.schedule_response()),
    (WebhookResponse, smoke.webhook_response()),
    (APIKeyResponse, smoke.api_key_response()),
    (APIKeyCreateResponse, smoke.api_key_create_response()),
    (ProjectsContextResponse, smoke.projects_context_response()),
    (ProjectSwitchResponse, smoke.project_switch_response()),
    (PricingCatalogResponse, smoke.pricing_catalog_response()),
    (BillingStatusResponse, smoke.billing_status_response()),
    (RateMeterResponse, smoke.rate_meter_response()),
    (AssetResponse, smoke.asset_response()),
    (AssetListResponse, smoke.asset_list_response()),
    (AssetDeleteResponse, smoke.asset_delete_response()),
    (BulkAssetDeleteResponse, smoke.bulk_asset_delete_response()),
    (BulkOperationResponse, smoke.bulk_operation_response()),
    (TeamMemberResponse, smoke.team_member_response()),
    (TeamMembersListResponse, smoke.team_members_list_response()),
    (TeamInvitationResponse, smoke.team_invitation_response()),
    (TeamInvitationsListResponse, smoke.team_invitations_list_response()),
    (MCPQuotaResponse, smoke.mcp_quota_response()),
    (EmailPreferencesResponse, smoke.email_preferences_response()),
]


@pytest.mark.parametrize("model, payload", CASES, ids=lambda v: getattr(v, "__name__", ""))
def test_fixture_validates_against_sdk_model(model, payload) -> None:
    # model_validate raises pydantic.ValidationError on any drift.
    model.model_validate(payload)
