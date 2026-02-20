from __future__ import annotations

import os
import re
import subprocess
from pathlib import Path

import anitopy
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser

from bot import settings


def _clean_name(name: str) -> str:
    cleaned = re.sub(r"[._]+", " ", name)
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    return cleaned


def build_renamed_filename(file_path: str | Path) -> str:
    """Return a readable file name generated from anime metadata."""
    source = Path(file_path)
    parsed = anitopy.parse(_clean_name(source.stem))

    title = parsed.get("anime_title") or source.stem
    parts = [f"[{title}]"]

    if parsed.get("anime_season"):
        parts.append(f"[Season {parsed['anime_season']}]")
    if parsed.get("episode_number"):
        parts.append(f"[Episode {parsed['episode_number']}]")

    parts.append(f"[{settings.suffix}]")
    return " ".join(parts) + ".mkv"


def get_thumbnail(input_file: str | Path) -> str:
    output_file = "thumb_auto.jpg"
    subprocess.run(
        [
            "ffmpeg",
            "-hide_banner",
            "-loglevel",
            "error",
            "-ss",
            "00:00:20",
            "-i",
            str(input_file),
            "-frames:v",
            "1",
            output_file,
            "-y",
        ],
        check=False,
    )
    return output_file


def get_duration(file_path: str | Path) -> int:
    parser = createParser(str(file_path))
    if not parser:
        return 0

    with parser:
        metadata = extractMetadata(parser)

    if metadata and metadata.has("duration"):
        return metadata.get("duration").seconds

    return 0


def get_width_height(file_path: str | Path) -> tuple[int, int]:
    parser = createParser(str(file_path))
    if not parser:
        return 1280, 720

    with parser:
        metadata = extractMetadata(parser)

    if metadata and metadata.has("width") and metadata.has("height"):
        return metadata.get("width"), metadata.get("height")

    return 1280, 720


def safe_remove(file_path: str | Path) -> None:
    try:
        os.remove(file_path)
    except FileNotFoundError:
        pass
