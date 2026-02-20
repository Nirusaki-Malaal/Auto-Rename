# Auto-Rename Telegram Bot

A Telegram bot for channel/admin workflows that renames anime/video files into a clean, consistent format before re-uploading.

## Features

- Queue-based processing (safe for multiple uploads).
- Cleaner and more informative bot UI messages.
- Auto filename parsing with `anitopy`:
  - Anime title
  - Season (if available)
  - Episode number (if available)
- Custom thumbnail support:
  - Send a photo once, saved as `thumb.jpg`.
- Automatic metadata extraction (duration, width, height).

## Filename Format

The bot generates names like:

```text
[Anime Title] [Season 1] [Episode 08] [YourSuffix].mkv
```

If parsing fails, the original stem is used.

## Requirements

- Python 3.10+
- `ffmpeg` available in PATH

## Setup

1. Clone this repo.
2. Install system dependency:

   ```bash
   sudo apt-get update && sudo apt-get install -y ffmpeg
   ```

3. Install Python dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Configure environment variables.

## Environment Variables

| Variable | Required | Description |
|---|---|---|
| `API_ID` | ✅ | Telegram API ID from https://my.telegram.org |
| `API_HASH` | ✅ | Telegram API hash from https://my.telegram.org |
| `BOT_TOKEN` | ✅ | Bot token from @BotFather |
| `SUDO_USERS` | ✅ | Space-separated Telegram user IDs allowed to use the bot |
| `SUFFIX` | ❌ | Tag appended to generated filename (default: `Renamed`) |
| `DOWNLOAD_DIR` | ❌ | Download directory (default: `downloads`) |

Example:

```env
API_ID=123456
API_HASH=your_api_hash
BOT_TOKEN=123456:ABCDEF
SUDO_USERS=11111111 22222222
SUFFIX=WEB-DL
DOWNLOAD_DIR=downloads
```

## Run

```bash
python -m bot
```

## Cleanup Done in This Revision

- Removed legacy platform files: `heroku.yml`, `app.json`.
- Removed duplicate/unused code paths and blocking queue logic.
- Standardized config loading and defaults.
- Improved readability and structure across core modules.

## License

MIT (see `LICENSE`).
