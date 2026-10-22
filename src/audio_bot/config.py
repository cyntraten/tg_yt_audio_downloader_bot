import os
import sys

from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("TG_BOT_TOKEN")
if not BOT_TOKEN:
  sys.stderr.write("TG_BOT_TOKEN is empty")
  sys.exit(1)
