import os
import logging
import asyncio
from pyrogram import Client, idle  # Import idle
from dotenv import load_dotenv
from nezukohelper.config import bot
from nezukohelper.utils.database import test_db_connection

# Setup logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Import ALL handlers
from nezukohelper.handlers import *

async def main():
    try:
        # Test MongoDB connection (await it properly)
        await test_db_connection()
        logger.info("🌸 Nezuko Helper Started!")
        
        # Start Pyrogram bot in async mode
        await bot.start()
        await idle()  # Keeps the bot running
    except Exception as e:
        logger.error(f"FATAL ERROR: {str(e)}")
    finally:
        await bot.stop()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())  # Correct way to run an async function
