from pyrogram.types import InlineKeyboardButton, User
from pyrogram import Client
import time
import logging
from typing import Optional, Union

logger = logging.getLogger(__name__)

def emoji(name: str) -> str:
    """Returns emoji by name with validation"""
    emojis = {
        "flower": "🌸",
        "warning": "⚠️",
        "ban": "🚫",
        "heart": "❤️",
        "dice": "🎲",
        "success": "✅",
        "error": "❌",
        "info": "ℹ️",
        "clock": "⏰"
    }
    return emojis.get(name.strip().lower(), "")

def create_button_row(*buttons: tuple[str, str]) -> list[InlineKeyboardButton]:
    """Create a row of buttons quickly"""
    return [InlineKeyboardButton(text, callback_data=data) for text, data in buttons]

def format_time(timestamp: float, timezone: str = "UTC") -> str:
    """Convert timestamp to formatted time with timezone"""
    try:
        return (datetime.fromtimestamp(timestamp)
                      .astimezone(ZoneInfo(timezone))
                      .strftime("%d %b %Y, %H:%M:%S"))
    except:
        return "Invalid timestamp"

async def parse_user(client: Client, text: str, message) -> Optional[User]:
    """Advanced user parser with error handling"""
    try:
        if message.reply_to_message:
            return message.reply_to_message.from_user
        
        if text.startswith("@"):
            return await client.get_users(text[1:])
        
        if text.isdigit():
            return await client.get_users(int(text))
        
        return None
    except Exception as e:
        logger.error(f"User parse error: {str(e)}")
        return None

async def log_error(client: Client, error: Exception, context: str = ""):
    """Enhanced error logging with traceback"""
    from nezukohelper.config import LOG_CHAT
    
    error_text = (
        f"{emoji('error')} **Error Report**\n\n"
        f"• Time: `{format_time(time.time())}`\n"
        f"• Context: `{context}`\n"
        f"• Error: `{str(error)[:2000]}`\n"
    )
    
    try:
        await client.send_message(
            LOG_CHAT,
            error_text,
            disable_web_page_preview=True
        )
    except Exception as e:
        logger.critical(f"Failed to log error: {str(e)}")
