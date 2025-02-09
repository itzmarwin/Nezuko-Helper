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
        test_db_connection()
        logger.info("🌸 Nezuko Helper Started!")
        bot.run()
    except Exception as e:
        logger.error(f"FATAL ERROR: {str(e)}")
