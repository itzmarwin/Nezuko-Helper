import os
import logging
import traceback
from pyrogram import idle
from dotenv import load_dotenv
from nezukohelper.config import bot
from nezukohelper.utils.database import init_db  # Updated import

# Logging Configuration
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

async def main():
    try:
        # Step 1: Load Environment Variables
        load_dotenv()
        logger.info("🌸 Environment variables loaded")

        # Step 2: Initialize Database First
        logger.info("🔌 Initializing database...")
        if not await init_db():
            logger.error("❌ Critical: DB Connection Failed!")
            return

        # Step 3: Import Handlers After DB Init
        logger.info("📦 Loading handlers...")
        from nezukohelper.handlers import (  # All handlers
            start, afk, stickers, group_stats,
            warn, zombies, filters, tagall,
            games, couple, broadcast, userinfo,
            gban, automod, leaderboard, ban
        )

        # Step 4: Start Bot
        logger.info("🚀 Starting bot...")
        await bot.start()

        # Step 5: Send Startup Notification
        await bot.send_message(
            os.getenv("LOG_CHAT"),  # Use configurable chat
            "🌸 **Bot Started Successfully!**"
        )

        # Step 6: Keep Running
        await idle()

    except Exception as e:
        logger.critical(f"🔥 Critical Error: {str(e)}")
        logger.error(traceback.format_exc())
    finally:
        if bot.is_connected:
            await bot.stop()
            logger.info("🌸 Bot stopped gracefully")

if __name__ == "__main__":
    asyncio.run(main())
