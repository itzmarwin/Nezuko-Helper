from pyrogram import filters
from nezukohelper.config import bot
from nezukohelper.utils.database import groups
from nezukohelper.utils.helpers import emoji
import os

@bot.on_message(filters.private & filters.command("start"))
async def log_bot_start(_, message):
    # Log new user
    log_text = (
        f"{emoji('🌸')} **New User Started Bot**\n"
        f"• User: {message.from_user.mention}\n"
        f"• ID: `{message.from_user.id}`\n"
        f"• Username: @{message.from_user.username}"
    )
    try:
        await bot.send_message(
            int(os.getenv("LOG_CHAT")),
            log_text
        )
    except Exception as e:
        print(f"Log Error: {e}")

@bot.on_message(filters.new_chat_members)
async def log_group_add(_, message):
    if bot.me.id in [user.id for user in message.new_chat_members]:
        # Log new group addition
        log_text = (
            f"{emoji('✨')} **Added to New Group**\n"
            f"• Title: {message.chat.title}\n"
            f"• ID: `{message.chat.id}`\n"
            f"• Added by: {message.from_user.mention}"
        )
        try:
            await bot.send_message(
                int(os.getenv("LOG_CHAT")),
                log_text
            )
            # Save group to DB
            await groups.update_one(
                {"chat_id": message.chat.id},
                {"$set": {"title": message.chat.title}},
                upsert=True
            )
        except Exception as e:
            print(f"Log Error: {e}")
