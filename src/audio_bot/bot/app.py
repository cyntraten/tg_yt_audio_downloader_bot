import logging

from telegram.ext import ApplicationBuilder, MessageHandler, filters

from src.audio_bot.bot.handlers import get_video_url
from src.audio_bot.config import BOT_TOKEN

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)


if __name__ == "__main__":
    application = ApplicationBuilder().token(BOT_TOKEN).build()
    get_video_url_handler = MessageHandler(
        filters.TEXT & (~filters.COMMAND), get_video_url
    )
    application.add_handler(get_video_url_handler)

    application.run_polling()
