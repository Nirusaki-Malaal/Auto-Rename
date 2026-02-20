from __future__ import annotations

import asyncio
import os
from collections import deque

from pyrogram.types import Message

from bot import app
from .ffmpeg_utils import (
    build_renamed_filename,
    get_duration,
    get_thumbnail,
    get_width_height,
    safe_remove,
)


task_queue: deque[Message] = deque()
queue_lock = asyncio.Lock()
worker_running = False


async def enqueue_task(message: Message) -> int:
    global worker_running

    async with queue_lock:
        task_queue.append(message)
        queue_position = len(task_queue)

        if not worker_running:
            worker_running = True
            asyncio.create_task(_queue_worker())

    return queue_position


async def _queue_worker() -> None:
    global worker_running

    while True:
        async with queue_lock:
            if not task_queue:
                worker_running = False
                return
            message = task_queue.popleft()

        await _process_message(message)


async def _process_message(message: Message) -> None:
    status = await message.reply_text("⬇️ Downloading your file...")
    downloaded_file = None
    auto_thumb = None

    try:
        downloaded_file = await message.download()
        final_name = build_renamed_filename(downloaded_file)

        await status.edit_text("📝 Renaming and preparing metadata...")

        width, height = get_width_height(downloaded_file)
        duration = get_duration(downloaded_file)

        thumb = "thumb.jpg"
        if not await _file_exists(thumb):
            auto_thumb = get_thumbnail(downloaded_file)
            thumb = auto_thumb

        await status.edit_text("⬆️ Uploading renamed file...")

        await app.send_video(
            chat_id=message.chat.id,
            video=downloaded_file,
            file_name=final_name,
            caption=f"✅ {final_name}",
            supports_streaming=True,
            thumb=thumb,
            width=width,
            height=height,
            duration=duration,
        )

        await status.edit_text("✅ Done.")
    except Exception as error:  # noqa: BLE001
        await status.edit_text(f"❌ Failed to process file: `{error}`")
    finally:
        if downloaded_file:
            safe_remove(downloaded_file)
        if auto_thumb:
            safe_remove(auto_thumb)


async def _file_exists(path: str) -> bool:
    return await asyncio.to_thread(os.path.exists, path)
