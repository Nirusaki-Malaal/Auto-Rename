from pyrogram import filters

from bot import app, settings
from bot.helper.utils import enqueue_task

VIDEO_MIME_TYPES = {
    "video/x-flv",
    "video/mp4",
    "application/x-mpegURL",
    "video/MP2T",
    "video/3gpp",
    "video/quicktime",
    "video/x-msvideo",
    "video/x-ms-wmv",
    "video/x-matroska",
    "video/webm",
    "video/x-m4v",
    "video/mpeg",
}


@app.on_message(filters.user(settings.sudo_users) & filters.command(["start", "help"]))
async def help_message(_, message):
    await message.reply_text(
        "👋 **Welcome to Auto Rename Bot**\n\n"
        "Send me a video file and I will:\n"
        "• Detect anime title/season/episode\n"
        "• Generate a clean filename\n"
        "• Upload the renamed file back\n\n"
        "Optional: send a photo to set `thumb.jpg` as your custom thumbnail."
    )


@app.on_message(filters.user(settings.sudo_users) & (filters.video | filters.document))
async def queue_video(_, message):
    if message.document and message.document.mime_type not in VIDEO_MIME_TYPES:
        await message.reply_text("❌ Unsupported file type. Please send a valid video file.")
        return

    position = await enqueue_task(message)
    await message.reply_text(f"📥 Added to queue. Position: **{position}**")


@app.on_message(filters.user(settings.sudo_users) & filters.photo)
async def set_thumbnail(_, message):
    await message.download(file_name="thumb.jpg")
    await message.reply_text("🖼️ Custom thumbnail saved as `thumb.jpg`.")


app.run()
