# python-examples

Examples aligned with PinBridge SDK v1.0.0.

Practical Python examples for the PinBridge SDK, covering every SDK resource:
system, auth, Pinterest, assets, pins/imports/jobs, schedules, webhooks, billing,
projects, API keys, and advanced client patterns.

## Prerequisites

- Python `>=3.10`
- A PinBridge account
- At least one connected Pinterest account in PinBridge
- Either a local image/video file to upload or a publicly accessible image URL for pin publishing

## Install Dependencies

Published SDK (PyPI):

```bash
pip install pinbridge-sdk>=1.0.0
```

PyPI project page:

- https://pypi.org/project/pinbridge-sdk/

Or install from this repo requirements file:

```bash
pip install -r requirements.txt
```

If you want to use local SDK code from this workspace instead of PyPI:

```bash
pip install -e ../python-sdk
```

## Example Catalog

Basic examples:

- `examples/health_root.py`:
  Check root, health, and readiness endpoints.
- `examples/system_readiness_and_webhooks.py`:
  Check readiness and optionally forward a Stripe webhook payload.
- `examples/auth_and_profile.py`:
  Log in with email/password and inspect the authenticated workspace/profile context.
- `examples/auth_full_lifecycle.py`:
  Demonstrate register, profile update, email verification, and password recovery/change APIs.
- `examples/pinterest_accounts_and_boards.py`:
  List connected Pinterest accounts and boards, with optional board create/delete steps.
- `examples/pinterest_oauth_callback_and_disconnect.py`:
  Run OAuth callback handling and optionally revoke a connected Pinterest account.
- `examples/publish_from_image_url.py`:
  Publish a pin from a hosted image URL.
- `examples/upload_and_publish_local_media.py`:
  Upload a local image or video and publish it as a pin.
- `examples/assets_retrieve_and_download.py`:
  Fetch asset metadata and download raw asset content bytes.
- `examples/pins_bulk_import_and_management.py`:
  Create/list/delete pins and run JSON/CSV import jobs with status lookups.
- `examples/schedules_lifecycle.py`:
  Create, fetch, list, and optionally cancel a schedule.
- `examples/webhooks_lifecycle.py`:
  Create, update, fetch, list, and delete a webhook.
- `examples/webhook_signature_verification.py`:
  Compute and verify `X-PinBridge-Signature` values locally.
- `examples/webhook_receiver.py`:
  Run a small local HTTP receiver that validates PinBridge webhook deliveries.
- `examples/billing_and_rate_meter.py`:
  Inspect pricing, billing status, and rate-meter capacity.
- `examples/billing_checkout_flow.py`:
  Generate a checkout URL for a requested plan and billing cycle.
- `examples/api_keys_lifecycle.py`:
  Create an API key, update its metadata, and revoke it.
- `examples/projects_sandbox.py`:
  List projects, ensure a sandbox exists, switch to it, and optionally reset it.

Advanced examples:

- `examples/auth_boards_publish_schedule.py`:
  End-to-end bearer-auth flow that creates a board, uploads media, publishes, and schedules.
- `examples/async_publish_workflow.py`:
  Async client example for publishing and scheduling with `AsyncPinbridgeClient`.
- `examples/advanced_client_patterns.py`:
  Use `with_options()`, low-level `request()`, and `register_resource()` for custom helpers.

Workflow recipes:

- `examples/recipe_shopify_product_publish.py`:
  Turn a Shopify product event into an idempotent publish call.
- `examples/recipe_cms_scheduled_pin.py`:
  Schedule a CMS article for Pinterest after editorial approval.
- `examples/recipe_multi_account_campaign.py`:
  Fan out the same campaign asset across multiple connected Pinterest accounts.

Tests:

- `tests/test_examples_smoke.py`:
  Pytest smoke coverage for the example scripts using `httpx.MockTransport`.

## Environment Variables

### Common

- `PINBRIDGE_BASE_URL`:
  API base URL. Defaults to `https://api.pinbridge.io`.
- `PINBRIDGE_API_KEY`:
  Required for most server-to-server examples.
- `PINBRIDGE_EMAIL`
- `PINBRIDGE_PASSWORD`:
  Required for bearer-auth examples.
- `PINBRIDGE_ACCOUNT_ID`:
  Optional. Select a specific connected Pinterest account.
- `PINBRIDGE_BOARD_ID`:
  Optional. Select a specific board. Otherwise the first board is used.
- `PINBRIDGE_LINK_URL`:
  Optional destination URL for pins/schedules.
- `PINBRIDGE_PIN_TITLE`
- `PINBRIDGE_PIN_DESCRIPTION`
- `PINBRIDGE_SCHEDULED_PIN_TITLE`
- `PINBRIDGE_SCHEDULED_PIN_DESCRIPTION`
- `PINBRIDGE_SCHEDULE_MINUTES`:
  Minutes from now for schedule examples. Defaults to `60`.

### Optional

- `PINBRIDGE_IMAGE_URL`:
  Required for `publish_from_image_url.py`.
- `PINBRIDGE_IMAGE_PATH`:
  Required for local image upload examples.
- `PINBRIDGE_VIDEO_PATH`:
  Required for local video upload examples.
- `PINBRIDGE_PROJECT_MODE`:
  Used by `auth_boards_publish_schedule.py`.
- `PINBRIDGE_BOARD_NAME`
- `PINBRIDGE_BOARD_DESCRIPTION`
- `PINBRIDGE_BOARD_PRIVACY`
- `PINBRIDGE_CREATE_BOARD=1`:
  Enable board creation in `pinterest_accounts_and_boards.py`.
- `PINBRIDGE_DELETE_CREATED_BOARD=1`:
  Delete the example board after creation.
- `PINBRIDGE_RESET_SANDBOX=1`:
  Reset the sandbox in `projects_sandbox.py`.
- `PINBRIDGE_FORWARD_STRIPE_WEBHOOK=1`:
  Enable webhook forwarding in `system_readiness_and_webhooks.py`.
- `PINBRIDGE_STRIPE_WEBHOOK_BODY`:
  Raw JSON payload for `system_readiness_and_webhooks.py`.
- `PINBRIDGE_STRIPE_SIGNATURE`:
  Stripe signature header value for `system_readiness_and_webhooks.py`.
- `PINBRIDGE_REGISTER_USER=1`:
  Use user registration flow in `auth_full_lifecycle.py`.
- `PINBRIDGE_REGISTER_FULL_NAME`
- `PINBRIDGE_REGISTER_EMAIL`
- `PINBRIDGE_REGISTER_PASSWORD`
- `PINBRIDGE_REGISTER_WORKSPACE_NAME`
- `PINBRIDGE_REGISTER_TIMEZONE`:
  Registration inputs for `auth_full_lifecycle.py` when register mode is enabled.
- `PINBRIDGE_UPDATE_PROFILE=1`:
  Enable profile update in `auth_full_lifecycle.py`.
- `PINBRIDGE_PROFILE_FULL_NAME`
- `PINBRIDGE_PROFILE_WORKSPACE_NAME`
- `PINBRIDGE_PROFILE_COMPANY_NAME`
- `PINBRIDGE_PROFILE_COMPANY_WEBSITE`
- `PINBRIDGE_PROFILE_BILLING_EMAIL`
- `PINBRIDGE_PROFILE_BILLING_PHONE`:
  Optional profile fields for `auth_full_lifecycle.py`.
- `PINBRIDGE_REQUEST_EMAIL_VERIFICATION=1`:
  Trigger verification email request in `auth_full_lifecycle.py`.
- `PINBRIDGE_EMAIL_VERIFICATION_TOKEN`:
  Verification token used by `auth_full_lifecycle.py`.
- `PINBRIDGE_REQUEST_PASSWORD_RESET=1`:
  Trigger forgot-password request in `auth_full_lifecycle.py`.
- `PINBRIDGE_PASSWORD_RESET_TOKEN`
- `PINBRIDGE_NEW_PASSWORD`:
  Reset-password inputs used by `auth_full_lifecycle.py`.
- `PINBRIDGE_CHANGE_PASSWORD=1`:
  Enable password change in `auth_full_lifecycle.py`.
- `PINBRIDGE_CURRENT_PASSWORD`
- `PINBRIDGE_NEXT_PASSWORD`:
  Change-password inputs used by `auth_full_lifecycle.py`.
- `PINBRIDGE_OAUTH_CODE`
- `PINBRIDGE_OAUTH_STATE`
- `PINBRIDGE_OAUTH_FOLLOW_REDIRECTS=1`:
  OAuth callback inputs for `pinterest_oauth_callback_and_disconnect.py`.
- `PINBRIDGE_REVOKE_ACCOUNT_ID`:
  Account id to revoke in `pinterest_oauth_callback_and_disconnect.py`.
- `PINBRIDGE_REVOKE_FIRST_ACCOUNT=1`:
  Revoke the first connected account in `pinterest_oauth_callback_and_disconnect.py`.
- `PINBRIDGE_ASSET_ID`:
  Existing asset id for `assets_retrieve_and_download.py`.
- `PINBRIDGE_ASSET_OUTPUT_PATH`:
  Optional local file path to write downloaded bytes in `assets_retrieve_and_download.py`.
- `PINBRIDGE_DELETE_CREATED_PIN=1`:
  Delete the created pin in `pins_bulk_import_and_management.py`.
- `PINBRIDGE_CANCEL_SCHEDULE=1`:
  Cancel the created schedule in `schedules_lifecycle.py`.
- `PINBRIDGE_WEBHOOK_URL`
- `PINBRIDGE_WEBHOOK_SECRET`:
  Required for `webhooks_lifecycle.py`, `webhook_signature_verification.py`, and `webhook_receiver.py`.
- `PINBRIDGE_WEBHOOK_BODY`:
  Optional raw JSON string for `webhook_signature_verification.py`.
- `PINBRIDGE_WEBHOOK_SIGNATURE`:
  Optional signature to validate in `webhook_signature_verification.py`.
- `PINBRIDGE_WEBHOOK_HOST`:
  Host bind address for `webhook_receiver.py`. Defaults to `127.0.0.1`.
- `PINBRIDGE_WEBHOOK_PORT`:
  Port for `webhook_receiver.py`. Defaults to `8787`.
- `PINBRIDGE_CREATE_PORTAL=1`:
  Generate a billing portal URL in `billing_and_rate_meter.py`.
- `PINBRIDGE_CHECKOUT_PLAN`:
  Target plan (`free|starter|growth|pro|enterprise`) for `billing_checkout_flow.py`.
- `PINBRIDGE_CHECKOUT_CYCLE`:
  Billing cycle (`monthly|annual`) for `billing_checkout_flow.py`.
- `SHOPIFY_PRODUCT_ID`
- `SHOPIFY_PRODUCT_TITLE`
- `SHOPIFY_PRODUCT_DESCRIPTION`
- `SHOPIFY_PRODUCT_URL`
- `SHOPIFY_IMAGE_URL`:
  Used by `recipe_shopify_product_publish.py`.
- `CMS_ARTICLE_SLUG`
- `CMS_ARTICLE_TITLE`
- `CMS_ARTICLE_DESCRIPTION`
- `CMS_ARTICLE_URL`
- `CMS_IMAGE_URL`:
  Used by `recipe_cms_scheduled_pin.py`.
- `PINBRIDGE_MAX_ACCOUNTS`:
  Limit for `recipe_multi_account_campaign.py`. Defaults to `3`.

## Run An Example

```bash
export PINBRIDGE_API_KEY="pb_live_or_sandbox_key"
export PINBRIDGE_PIN_TITLE="Spring drop"
export PINBRIDGE_IMAGE_URL="https://images.example.com/pin.jpg"

python examples/publish_from_image_url.py
```

Bearer-auth example:

```bash
export PINBRIDGE_EMAIL="you@example.com"
export PINBRIDGE_PASSWORD="your-password"

python examples/auth_and_profile.py
```

Async example:

```bash
export PINBRIDGE_API_KEY="pb_live_or_sandbox_key"
export PINBRIDGE_IMAGE_PATH="/absolute/path/to/pin-image.png"

python examples/async_publish_workflow.py
```

Webhook verification example:

```bash
export PINBRIDGE_WEBHOOK_SECRET="0123456789012345"
export PINBRIDGE_WEBHOOK_BODY='{"pin_id":"demo","status":"published"}'

python examples/webhook_signature_verification.py
```

Local receiver example:

```bash
export PINBRIDGE_WEBHOOK_SECRET="0123456789012345"

python examples/webhook_receiver.py
```

Run smoke tests:

```bash
pytest tests -q
```

## Expected Behavior

Each script prints the resource IDs, statuses, or URLs returned by the API for the flow it demonstrates.

Examples that create temporary resources generally clean up after themselves when that makes sense,
such as revoking API keys or deleting webhook endpoints. For stateful resources like boards and
schedules, cleanup is exposed through opt-in environment flags.

Webhook handling examples are local-only utilities. They do not call the PinBridge API and are
meant to show how to validate webhook deliveries safely before wiring them into your app.

If no Pinterest account is connected, it prints an OAuth URL and exits so you can connect an account first.

## Troubleshooting

- `Missing required environment variable`: define the variable and rerun.
- `API error [401] ...`: verify credentials/token and workspace access.
- `Pinterest account not found`: connect an account or provide a valid `PINBRIDGE_ACCOUNT_ID`.
- Media validation/publish errors: verify local image/video paths point to real files or `PINBRIDGE_IMAGE_URL` is publicly accessible and valid.
- `No boards found`: create a board first, set `PINBRIDGE_BOARD_ID`, or run `examples/pinterest_accounts_and_boards.py`.
- `Expected exactly one media input`: set only one of `PINBRIDGE_IMAGE_URL`, `PINBRIDGE_IMAGE_PATH`, or `PINBRIDGE_VIDEO_PATH`.
