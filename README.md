# python-examples

Practical Python examples for the PinBridge SDK.

## Prerequisites

- Python `>=3.10`
- A PinBridge account
- At least one connected Pinterest account in PinBridge
- A publicly accessible image URL for pin publishing

## Install Dependencies

Published SDK (PyPI):

```bash
pip install pinbridge-sdk>=0.1.3
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
4. Publish a pin immediately
5. Schedule another pin for later

## Environment Variables

### Required

- `PINBRIDGE_EMAIL`
- `PINBRIDGE_PASSWORD`
- `PINBRIDGE_IMAGE_URL` (must be reachable by Pinterest)

### Optional

- `PINBRIDGE_BASE_URL` (default: `https://api.pinbridge.io`)
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
export PINBRIDGE_IMAGE_URL="https://images.example.com/pin.jpg"

python examples/auth_boards_publish_schedule.py
```

## Expected Behavior

The script prints each stage:

- authentication result
- selected Pinterest account
- existing boards
- created board details
- published pin id + status
- created schedule id + run time

If no Pinterest account is connected, it prints an OAuth URL and exits so you can connect an account first.

## Troubleshooting

- `Missing required environment variable`: define the variable and rerun.
- `API error [401] ...`: verify credentials/token and workspace access.
- `Pinterest account not found`: connect an account or provide a valid `PINBRIDGE_ACCOUNT_ID`.
- Image validation/publish errors: verify `PINBRIDGE_IMAGE_URL` is publicly accessible and valid.
