import os
import logging
import traceback
from pyrogram import Client
from dotenv import load_dotenv
from nezukohelper.utils.database import test_db_connection
from nezukohelper.config import bot

# Logging Configuration
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
    handlers=[
        logging.StreamHandler(),  # Logs to console
    ]
)
logger = logging.getLogger(__name__)

async def main():
    try:
        # Load Environment Variables
        load_dotenv()
        logger.info("🌸 Loading environment variables...")

        # Test MongoDB Connection
        logger.info("🔌 Testing MongoDB connection...")
        db_status = await test_db_connection()
        if not db_status:
            logger.error("❌ MongoDB Connection Failed! Exiting...")
            return

        # Import All Handlers
        logger.info("📦 Importing handlers...")
        from nezukohelper.handlers import (  # Explicit imports
            afk, stickers, warn, group_stats, zombies,
            filters, tagall, games, couple, sudo,
            broadcast, userinfo, gban, automod,
            logging, start, leaderboard, ban, logger_group
        )

        # Start the Bot
        logger.info("🚀 Starting Nezuko Helper Bot...")
        await bot.start()
        
        # Send test message to yourself
        await bot.send_message("me", "🌸 **Bot Started Successfully!**")
        logger.info("✅ Bot is active! Sent confirmation message.")
        
        # Keep the bot running
        await bot.run()

    except Exception as e:
        logger.critical(f"🔥 CRITICAL ERROR: {str(e)}")
        logger.error(traceback.format_exc())  # Print full traceback
    finally:
        if await bot.is_connected:
            logger.info("🛑 Stopping bot...")
            await bot.stop()
            logger.info("🌸 Bot stopped gracefully.")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
