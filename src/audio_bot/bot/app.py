import logging

from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters

from src.audio_bot.bot.handlers import get_audio, start
from src.audio_bot.config import BOT_TOKEN

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)


if __name__ == "__main__":
    application = ApplicationBuilder().token(BOT_TOKEN).build()
    get_audio_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), get_audio)
    start_handler = CommandHandler("start", start)
    application.add_handler(get_audio_handler)
    application.add_handler(start_handler)

    application.run_polling()
