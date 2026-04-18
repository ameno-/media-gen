#!/usr/bin/env python3
"""
OpenRouter Image Generation Adapter

Standalone image generation via OpenRouter API.
Works with Nano Banana (Gemini 2.5 Flash Image) and other models.

Usage:
    python openrouter_image.py "Your prompt" -o output.png
    python openrouter_image.py "Your prompt" -o output.png -m google/gemini-2.5-flash-image-preview -a 16:9

Environment:
    OPENROUTER_API_KEY - Required. Get from https://openrouter.ai/keys
"""

import argparse
import base64
import os
import sys
import json
import logging
import tempfile
import httpx
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path

logger = logging.getLogger(__name__)


class ImageModel(str, Enum):
    NANO_BANANA = "google/gemini-2.5-flash-image-preview"
    NANO_BANANA_PRO = "google/gemini-2.0-flash-image-generation"
    FLUX_MAX = "black-forest-labs/flux-2-max"
    FLUX_FLEX = "black-forest-labs/flux-2-flex"
    GPT5_IMAGE = "openai/gpt-5-image"
    GPT5_IMAGE_MINI = "openai/gpt-5-image-mini"


class AspectRatio(str, Enum):
    SQUARE = "1:1"
    LANDSCAPE = "16:9"
    PORTRAIT = "9:16"
    WIDE = "21:9"
    TALL = "9:21"
    STANDARD_4_3 = "4:3"
    STANDARD_3_4 = "3:4"


class ImageSize(str, Enum):
    SIZE_1K = "1K"
    SIZE_2K = "2K"
    SIZE_4K = "4K"


@dataclass
class ImageConfig:
    model: ImageModel = ImageModel.NANO_BANANA
    aspect_ratio: AspectRatio = AspectRatio.LANDSCAPE
    image_size: ImageSize = ImageSize.SIZE_2K
    temperature: float = 1.0
    max_tokens: int = 8192


@dataclass
class ImageResult:
    success: bool
    file_path: str | None = None
    base64_data: str | None = None
    text_response: str | None = None
    error: str | None = None
    model_used: str | None = None


def get_api_key() -> str:
    key = os.getenv("OPENROUTER_API_KEY")
    if not key:
        raise RuntimeError(
            "OPENROUTER_API_KEY not set. "
            "Get your key at https://openrouter.ai/keys"
        )
    return key


def extract_image_data(response_data: dict) -> tuple[str | None, str | None]:
    """Extract base64 image and text from API response."""
    base64_data, text_response = None, None

    choices = response_data.get("choices", [])
    if not choices:
        return None, None

    message = choices[0].get("message", {})
    content = message.get("content")

    if isinstance(content, str):
        text_response = content
    elif isinstance(content, list):
        for part in content:
            if isinstance(part, dict):
                if part.get("type") == "text":
                    text_response = part.get("text", "")
                elif part.get("type") == "image_url":
                    url = part.get("image_url", {}).get("url", "")
                    if url.startswith("data:image"):
                        base64_data = url.split(",", 1)[1] if "," in url else url

    # Also check Gemini-style images array
    images = message.get("images", [])
    if images and not base64_data:
        first = images[0]
        if isinstance(first, dict):
            url = first.get("image_url", {}).get("url", "")
            if url.startswith("data:image"):
                base64_data = url.split(",", 1)[1] if "," in url else url
        elif isinstance(first, str) and first.startswith("data:image"):
            base64_data = first.split(",", 1)[1] if "," in first else first

    return base64_data, text_response


def save_image(base64_data: str, output_path: str) -> str:
    """Save base64 image data to file."""
    output_path = os.path.abspath(output_path)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    image_bytes = base64.b64decode(base64_data)
    with open(output_path, "wb") as f:
        f.write(image_bytes)
    return output_path


def generate_image(
    prompt: str,
    output_path: str | None = None,
    config: ImageConfig | None = None,
    timeout: float = 120.0,
) -> ImageResult:
    """Generate an image via OpenRouter API."""
    if config is None:
        config = ImageConfig()

    api_key = get_api_key()

    # Determine output path
    if output_path is None:
        fd, output_path = tempfile.mkstemp(suffix=".png")
        os.close(fd)

    # Build request
    payload = {
        "model": config.model.value,
        "messages": [{"role": "user", "content": prompt}],
        "modalities": ["image", "text"],
        "max_tokens": config.max_tokens,
        "temperature": config.temperature,
    }

    # Add image_config for Gemini models
    if config.model in (ImageModel.NANO_BANANA, ImageModel.NANO_BANANA_PRO):
        payload["image_config"] = {
            "aspect_ratio": config.aspect_ratio.value,
            "image_size": config.image_size.value,
        }

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://github.com/ameno-/media-gen",
        "X-Title": "media-gen",
    }

    try:
        with httpx.Client(timeout=timeout) as client:
            response = client.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers=headers,
                json=payload,
            )

            if response.status_code == 429:
                return ImageResult(success=False, error="Rate limit exceeded")
            if response.status_code != 200:
                return ImageResult(
                    success=False,
                    error=f"API error {response.status_code}: {response.text}",
                )

            response_data = response.json()

    except httpx.TimeoutException:
        return ImageResult(success=False, error=f"Request timed out after {timeout}s")
    except httpx.HTTPError as e:
        return ImageResult(success=False, error=f"HTTP error: {e}")

    base64_data, text_response = extract_image_data(response_data)

    if not base64_data:
        return ImageResult(
            success=False,
            error="No image data in response",
            text_response=text_response,
        )

    try:
        saved_path = save_image(base64_data, output_path)
    except Exception as e:
        return ImageResult(
            success=False,
            error=f"Failed to save image: {e}",
            text_response=text_response,
        )

    usage = response_data.get("usage", {})
    return ImageResult(
        success=True,
        file_path=saved_path,
        base64_data=base64_data,
        text_response=text_response,
        model_used=config.model.value,
    )


# --- CLI ---
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate images via OpenRouter API")
    parser.add_argument("prompt", help="Image generation prompt")
    parser.add_argument("-o", "--output", default="generated_image.png", help="Output file")
    parser.add_argument("-m", "--model", default=ImageModel.NANO_BANANA.value,
                        choices=[m.value for m in ImageModel], help="Model")
    parser.add_argument("-a", "--aspect-ratio", default=AspectRatio.LANDSCAPE.value,
                        choices=[r.value for r in AspectRatio], help="Aspect ratio")
    parser.add_argument("-s", "--size", default=ImageSize.SIZE_2K.value,
                        choices=[s.value for s in ImageSize], help="Image size")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")

    args = parser.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(message)s",
    )

    model = ImageModel(args.model)
    aspect = AspectRatio(args.aspect_ratio)
    size = ImageSize(args.size)

    config = ImageConfig(model=model, aspect_ratio=aspect, image_size=size)

    print(f"Generating with {model.value}...")
    result = generate_image(args.prompt, args.output, config)

    if result.success:
        print(f"✓ Saved to: {result.file_path}")
        if result.text_response:
            print(f"  Response: {result.text_response[:200]}")
    else:
        print(f"✗ Failed: {result.error}")
        sys.exit(1)
