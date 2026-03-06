"""Retrieve asset metadata/content, optionally uploading first."""

from __future__ import annotations

import os

from _common import make_sync_client, run_sync_example, upload_local_asset


def main() -> int:
    with make_sync_client(require_api_key=True) as client:
        asset_id = os.getenv("PINBRIDGE_ASSET_ID")
        if asset_id:
            source = f"existing asset {asset_id}"
        else:
            media = upload_local_asset(client)
            if media.asset_id is None:
                raise RuntimeError("Expected an uploaded asset id, but none was returned")
            asset_id = str(media.asset_id)
            source = media.source_label

        asset = client.assets.get(asset_id)
        content = client.assets.get_content(asset.id)

    print(f"Source: {source}")
    print(f"Asset id: {asset.id} ({asset.asset_type.value})")
    print(f"Original filename: {asset.original_filename}")
    print(f"Downloaded bytes: {len(content)}")

    output_path = os.getenv("PINBRIDGE_ASSET_OUTPUT_PATH")
    if output_path:
        with open(output_path, "wb") as file_handle:
            file_handle.write(content)
        print(f"Wrote asset content to: {output_path}")
    else:
        print("Skipping file output. Set PINBRIDGE_ASSET_OUTPUT_PATH to write downloaded bytes.")

    return 0


if __name__ == "__main__":
    run_sync_example(main)
