import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv
from pyrogram import Client

load_dotenv()


@dataclass(frozen=True)
class Settings:
    api_id: int
    api_hash: str
    bot_token: str
    sudo_users: set[int]
    download_dir: Path
    suffix: str


def _load_settings() -> Settings:
    api_id = int(os.environ["API_ID"])
    api_hash = os.environ["API_HASH"]
    bot_token = os.environ["BOT_TOKEN"]
    sudo_users = {int(user_id) for user_id in os.environ["SUDO_USERS"].split()}
    download_dir = Path(os.environ.get("DOWNLOAD_DIR", "downloads")).expanduser()
    suffix = os.environ.get("SUFFIX", "Renamed")

    download_dir.mkdir(parents=True, exist_ok=True)

    return Settings(
        api_id=api_id,
        api_hash=api_hash,
        bot_token=bot_token,
        sudo_users=sudo_users,
        download_dir=download_dir,
        suffix=suffix,
    )


settings = _load_settings()

app = Client(
    name="auto-rename-bot",
    api_id=settings.api_id,
    api_hash=settings.api_hash,
    bot_token=settings.bot_token,
    workers=4,
)
