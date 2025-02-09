import os
import logging
from pyrogram import Client
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

if __name__ == "__main__":
    try:
        # Test MongoDB connection
        is_db_connected = await test_db_connection()  # ✅ await जरूरी है
        if not is_db_connected:
            logger.error("❌ MongoDB Connection Failed! Exiting...")
            exit(1)
        logger.info("🌸 Nezuko Helper Started!")
        await bot.run()  # ✅ await जोड़ें
    except Exception as e:
        logger.error(f"FATAL ERROR: {str(e)}")
