# python-examples

Examples aligned with PinBridge SDK v1.0.0.

Practical Python examples for the PinBridge SDK.

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

## Example Included

- `examples/auth_boards_publish_schedule.py`

This example demonstrates a complete flow:

1. Authenticate with email/password
2. List connected Pinterest boards
3. Create a new board
4. Upload an image or video asset when using a local file
5. Publish a pin immediately
6. Schedule another pin for later

## Environment Variables

### Required

- `PINBRIDGE_EMAIL`
- `PINBRIDGE_PASSWORD`
- `PINBRIDGE_IMAGE_PATH`, `PINBRIDGE_VIDEO_PATH`, or `PINBRIDGE_IMAGE_URL`

### Optional

- `PINBRIDGE_BASE_URL` (default: `https://api.pinbridge.io`)
- `PINBRIDGE_PROJECT_MODE` (`production` default, set `sandbox` to create/switch sandbox project)
- `PINBRIDGE_LINK_URL` (destination URL for pins)
- `PINBRIDGE_ACCOUNT_ID` (select a specific connected Pinterest account)
- `PINBRIDGE_BOARD_NAME`
- `PINBRIDGE_BOARD_DESCRIPTION`
- `PINBRIDGE_BOARD_PRIVACY`
- `PINBRIDGE_PIN_TITLE`
- `PINBRIDGE_PIN_DESCRIPTION`
- `PINBRIDGE_SCHEDULED_PIN_TITLE`
- `PINBRIDGE_SCHEDULED_PIN_DESCRIPTION`
- `PINBRIDGE_SCHEDULE_MINUTES` (default: `60`)

## Run the Example

```bash
export PINBRIDGE_EMAIL="you@example.com"
export PINBRIDGE_PASSWORD="your-password"
export PINBRIDGE_VIDEO_PATH="/absolute/path/to/pin-video.mp4"

python examples/auth_boards_publish_schedule.py
```

## Expected Behavior

The script prints each stage:

- authentication result
- selected Pinterest account
- existing boards
- created board details
- uploaded asset id when `PINBRIDGE_IMAGE_PATH` or `PINBRIDGE_VIDEO_PATH` is used
- published pin id + status
- created schedule id + run time

If no Pinterest account is connected, it prints an OAuth URL and exits so you can connect an account first.

## Troubleshooting

- `Missing required environment variable`: define the variable and rerun.
- `API error [401] ...`: verify credentials/token and workspace access.
- `Pinterest account not found`: connect an account or provide a valid `PINBRIDGE_ACCOUNT_ID`.
- Media validation/publish errors: verify local image/video paths point to real files or `PINBRIDGE_IMAGE_URL` is publicly accessible and valid.
