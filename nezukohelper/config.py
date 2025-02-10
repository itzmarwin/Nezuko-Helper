import os
from pyrogram import Client
from dotenv import load_dotenv

load_dotenv()  # .env file load करें

# Pyrogram Client Configuration
bot = Client(
    "NezukoHelper",
    api_id=int(os.getenv("API_ID")),  # API_ID must be integer
    api_hash=os.getenv("API_HASH"),
    bot_token=os.getenv("BOT_TOKEN"),
    in_memory=True  # Session को memory में रखेगा
)

# MongoDB Configuration (अलग file में होना चाहिए)
MONGO_URI = os.getenv("MONGO_URI")
LOG_CHAT = os.getenv("LOG_CHAT")  # String के रूप में लें

async def test_db_connection():
    """Database connection को utils/database.py में shift करें"""
    from motor.motor_asyncio import AsyncIOMotorClient
    try:
        client = AsyncIOMotorClient(MONGO_URI)
        await client.admin.command('ping')
        return True
    except Exception as e:
        print(f"MongoDB Connection Failed: {str(e)}")
        return False
