"""
Business logic for downloading One Piece Card Game card data
from the public OPTCG API.

No user interaction (no input/print) should be here.
"""

from __future__ import annotations

import json
import os
from typing import Any, Dict, List

import requests

BASE_URL = "https://optcgapi.com/api"


class CardNotFoundError(Exception):
    """Raised when the OPTCG API returns 404 for a card ID."""
    pass


def get_card_data(card_id: str) -> List[Dict[str, Any]]:
    """
    Fetch card data for a given card ID, e.g. 'OP01-001'.

    Returns a list of dicts. Each dict corresponds to a version of the card
    (regular, parallel art, etc.).
    """
    normalized = card_id.strip().upper()
    if not normalized:
        raise ValueError("Empty card ID.")

    url = f"{BASE_URL}/sets/card/{normalized}/"
    response = requests.get(url, timeout=10)

    # Give a clear error if the card ID doesn't exist
    if response.status_code == 404:
        raise CardNotFoundError(
            f"Card ID '{normalized}' was not found in the OPTCG API."
        )

    response.raise_for_status()

    data = response.json()
    if not isinstance(data, list):
        raise ValueError(f"Unexpected response format: {type(data)}")

    return data


def save_card_json(card_id: str,
                   data: List[Dict[str, Any]],
                   output_dir: str = "onepiece_cards") -> str:
    """
    Save the card data as pretty-printed JSON.

    File name: <card_id>.json inside output_dir.
    Returns the path to the saved file.
    """
    os.makedirs(output_dir, exist_ok=True)

    safe_id = card_id.replace("/", "_").replace("\\", "_").upper()
    path = os.path.join(output_dir, f"{safe_id}.json")

    with open(path, "w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=2, sort_keys=True)

    return path


def download_card_images(data: List[Dict[str, Any]],
                         output_dir: str = "onepiece_cards/images") -> List[str]:
    """
    Download images for all card versions in `data`, if image URLs are present.

    Returns a list of file paths saved.
    """
    os.makedirs(output_dir, exist_ok=True)

    saved_paths: List[str] = []

    for card in data:
        img_url = card.get("card_image")
        img_id = card.get("card_image_id")

        if not img_url or not img_id:
            continue

        resp = requests.get(img_url, timeout=10)
        resp.raise_for_status()

        # Try to guess extension from URL, fallback to .jpg
        _, ext = os.path.splitext(img_url)
        if not ext:
            ext = ".jpg"

        filename = f"{img_id}{ext}"
        path = os.path.join(output_dir, filename)

        with open(path, "wb") as img_file:
            img_file.write(resp.content)

        saved_paths.append(path)

    return saved_paths
