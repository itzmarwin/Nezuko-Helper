import os
from pyrogram import Client
from dotenv import load_dotenv

load_dotenv()  # Load .env file

# Initialize Pyrogram Client
bot = Client(
    "NezukoHelper",
    api_id=int(os.getenv("API_ID")),
    api_hash=os.getenv("API_HASH"),
    bot_token=os.getenv("BOT_TOKEN")
)

# MongoDB Configuration
MONGO_URI = os.getenv("MONGO_URI")
LOG_CHAT = int(os.getenv("LOG_CHAT", -1001234567890))  # Default log chat ID

async def test_db_connection():
    try:
        from motor.motor_asyncio import AsyncIOMotorClient
        client = AsyncIOMotorClient(MONGO_URI)
        await client.admin.command('ping')
        print("🌸 MongoDB Connection Verified!")
        return True
    except Exception as e:
        print(f"❌ MongoDB Error: {str(e)}")
        return False
