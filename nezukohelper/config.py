import os
from pyrogram import Client
from dotenv import load_dotenv

load_dotenv()

bot = Client(
    "NezukoHelper",
    api_id=int(os.getenv("API_ID")),
    api_hash=os.getenv("API_HASH"),
    bot_token=os.getenv("BOT_TOKEN")
)
