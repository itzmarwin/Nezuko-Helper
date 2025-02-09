import os
import logging
import asyncio
from pyrogram import Client
from dotenv import load_dotenv
from nezukohelper.utils.database import test_db_connection

# Configure logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Initialize Bot
bot = Client(
    "NezukoHelper",
    api_id=int(os.getenv("API_ID")),
    api_hash=os.getenv("API_HASH"),
    bot_token=os.getenv("BOT_TOKEN")
)

# Import ALL handlers
from nezukohelper.handlers import *

async def main():
    try:
        # Test MongoDB connection
        is_db_ok = await test_db_connection()
        if not is_db_ok:
            logger.error("❌ MongoDB Connection Failed! Shutting down...")
            return
        
        logger.info("🌸 Nezuko Helper Started!")
        await bot.start()
        await asyncio.Event().wait()  # Run indefinitely
        
    except Exception as e:
        logger.error(f"FATAL ERROR: {str(e)}")
    finally:
        if await bot.stop():
            logger.info("🌸 Bot stopped gracefully!")

if __name__ == "__main__":
    asyncio.run(main())
