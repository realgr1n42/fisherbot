from os import getenv

from dotenv import load_dotenv

load_dotenv()

# telegram bot token
TOKEN = getenv("BOT_TOKEN")

ONLYFISH_API_URL = getenv("ONLYFISH_API_URL")

ADMIN_PASSWORD = getenv("ADMIN_PASSWORD")

SUPER_ADMIN_USER_ID = 7429135349

EXPORTS_FOLDER = './exports'