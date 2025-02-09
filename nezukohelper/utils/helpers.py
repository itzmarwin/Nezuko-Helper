from pyrogram.types import InlineKeyboardButton
import time

def emoji(name: str) -> str:
    """Returns emoji by name (for cute responses)"""
    emojis = {
        "flower": "🌸",
        "warning": "⚠️",
        "ban": "🚫",
        "heart": "❤️",
        "dice": "🎲",
        "success": "✅",
        "error": "❌"
    }
    return emojis.get(name, "")

def create_button(text: str, data: str) -> InlineKeyboardButton:
    """Quickly create inline keyboard buttons"""
    return InlineKeyboardButton(text, callback_data=data)

def format_time(timestamp: float) -> str:
    """Convert Unix timestamp to readable time"""
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(timestamp))

async def parse_user(message, text: str):
    """Extract user from message text (supports ID/username/reply)"""
    try:
        if message.reply_to_message:
            return message.reply_to_message.from_user
        elif text.startswith("@"):
            return await bot.get_users(text[1:])
        else:
            return await bot.get_users(int(text))
    except:
        return None

async def log_error(error: Exception, context: str = ""):
    """Send error logs to LOG_CHAT"""
    from nezukohelper.config import LOG_CHAT
    error_text = (
        f"{emoji('⚠️')} **Error Report**\n\n"
        f"• Context: `{context}`\n"
        f"• Error: `{str(error)}`"
    )
    try:
        await bot.send_message(LOG_CHAT, error_text)
    except:
        pass
