from urllib.parse import urlsplit

from telegram import Update
from telegram.ext import ContextTypes

ALLOWED_SCHEMES = {"https"}
ALLOWED_DOMAINS = {"youtube.com", "www.youtube.com", "m.youtube.com", "youtu.be"}

async def get_video_url(update: Update, context: ContextTypes.DEFAULT_TYPE):
  if not update.message or not update.message.text:
    return
  url = update.message.text.strip()
  parsed_url = urlsplit(url)
  print(parsed_url)
  if parsed_url.scheme in ALLOWED_SCHEMES and parsed_url.netloc in ALLOWED_DOMAINS:
    await update.message.reply_text("Link is accepted, download audio...")
    print(f"Url to yt-dlp:{url}")
  else:
    await update.message.reply_text("Link is not supported, please send link to youtube")
    print(f"Url not youtube link:{url}")
