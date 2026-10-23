import asyncio
import logging
from pathlib import Path
from urllib.parse import urlsplit

from telegram import Update
from telegram.error import TelegramError
from telegram.ext import ContextTypes
from yt_dlp.utils import DownloadError

from src.audio_bot.services.downloader import AudioDownloader

ALLOWED_SCHEMES = {"https"}
ALLOWED_DOMAINS = {"youtube.com", "www.youtube.com", "m.youtube.com", "youtu.be"}
logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
  if not update.message or not update.message.text:
    return
  await update.message.reply_text("Hello, i am download audio from link to youtube, send me video :)")

async def get_audio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return
    url = update.message.text.strip()
    parsed_url = urlsplit(url)
    if (
        parsed_url.scheme not in ALLOWED_SCHEMES
        or parsed_url.netloc not in ALLOWED_DOMAINS
    ):
        await update.message.reply_text(
            "Link is not supported, please send link to youtube"
        )
        return

    status_msg = await update.message.reply_text(
        "Checking link...", reply_to_message_id=update.message.message_id
    )

    audio_path: Path | None = None
    try:
        audio_downloader = AudioDownloader()
        audio_metadata = await asyncio.to_thread(audio_downloader.extract_metadata, url)

        if int(audio_metadata["duration"]) > 3100:
            await status_msg.edit_text(
                "Maximum video duration 50 minutes(telegram file size limit), send another video"
            )
            return

        await status_msg.edit_text("Link is accepted, download audio...")

        audio_path = await asyncio.to_thread(audio_downloader.download_audio, url)
        await update.message.reply_audio(
            audio_path,
            title=audio_metadata["title"],
            performer=audio_metadata["uploader"],
            reply_to_message_id=update.message.message_id,
        )
        await status_msg.delete()

    except DownloadError as e:
        await status_msg.edit_text("Download audio error, try again later.")
        logger.error(f"yt-dlp downloading video error {url}: {e}")

    except TelegramError as e:
      await status_msg.edit_text("Download audio error, try again later.")
      logger.error(f"Telegram API error for video {url}: {e}")

    finally:
        if audio_path and audio_path.exists():
            audio_path.unlink(missing_ok=True)
            logger.info(f"File {audio_path} has been deleted")
