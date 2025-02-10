import os
import logging
import traceback
from pyrogram import idle  # Pyrogram के लिए ज़रूरी
from dotenv import load_dotenv
from nezukohelper.utils.database import test_db_connection
from nezukohelper.config import bot

# Logging Configuration
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

async def main():
    try:
        # Load Environment Variables
        load_dotenv()
        logger.info("🌸 Loading environment variables...")

        # MongoDB Connection Test
        logger.info("🔌 Testing MongoDB connection...")
        if not await test_db_connection():
            logger.error("❌ MongoDB Connection Failed! Exiting...")
            return

        # Import Handlers (Register करने के लिए)
        logger.info("📦 Importing and registering handlers...")
        from nezukohelper.handlers import (
            start, afk, stickers, group_stats  # और अन्य ज़रूरी handlers
        )

        # Start the Bot
        logger.info("🚀 Starting Nezuko Helper Bot...")
        await bot.start()

        # Send startup message
        await bot.send_message("me", "🌸 **Bot Started Successfully!**")
        logger.info("✅ Bot is active!")

        # Keep the bot running
        await idle()  # Pyrogram के लिए सही method

    except Exception as e:
        logger.critical(f"🔥 CRITICAL ERROR: {str(e)}")
        logger.error(traceback.format_exc())
    finally:
        if bot.is_connected:
            logger.info("🛑 Stopping bot...")
            await bot.stop()
            logger.info("🌸 Bot stopped gracefully.")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
