from pyrogram import filters
from nezukohelper.config import bot
from nezukohelper.utils.database import groups
from nezukohelper.utils.helpers import emoji
import os

async def send_log(action: str, admin: str, target: str, chat_title: str, reason: str = ""):
    log_text = (
        f"{emoji('📜')} **Action Logged**\n"
        f"• **Action:** `{action}`\n"
        f"• **Admin:** {admin}\n"
        f"• **Target:** {target}\n"
        f"• **Group:** {chat_title}\n"
        f"• **Reason:** {reason or 'Not specified'}"
    )
    try:
        await bot.send_message(
            int(os.getenv("LOG_CHAT")),
            log_text,
            disable_web_page_preview=True
        )
    except Exception as e:
        print(f"Log Error: {e}")

# ========== LOG BANS/WARNS/MUTES ==========
@bot.on_message(filters.command(["ban", "warn", "mute"]) & filters.group)
async def log_admin_actions(_, message):
    if not message.reply_to_message:
        return

    admin = message.from_user.mention
    target = message.reply_to_message.from_user.mention
    reason = " ".join(message.text.split()[2:]) if len(message.text.split()) > 2 else ""
    
    await send_log(
        action=message.command[0].capitalize(),
        admin=admin,
        target=target,
        chat_title=message.chat.title,
        reason=reason
    )

# ========== LOG SUDO COMMANDS ==========
@bot.on_message(filters.command(["addsudo", "rmsudo"]) & filters.private)
async def log_sudo_commands(_, message):
    target = " ".join(message.text.split()[1:]) if len(message.text.split()) > 1 else "Unknown"
    await send_log(
        action=f"Sudo {message.command[0]}",
        admin=message.from_user.mention,
        target=target,
        chat_title="Private Chat"
    )
