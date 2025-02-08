from pyrogram import filters
from nezukohelper.config import bot
from nezukohelper.utils.database import warns
from nezukohelper.utils.helpers import emoji
from datetime import datetime

@bot.on_message(filters.command("info") & filters.group)
async def user_info(_, message):
    # Get target user
    target = None
    if message.reply_to_message:
        target = message.reply_to_message.from_user
    elif len(message.command) > 1:
        try:
            user_input = message.text.split()[1]
            if user_input.startswith("@"):
                target = await bot.get_users(user_input)
            else:
                target = await bot.get_users(int(user_input))
        except:
            return await message.reply(f"{emoji('⚠️')} Invalid user!")
    else:
        target = message.from_user

    if not target:
        return await message.reply(f"{emoji('⚠️')} User not found!")

    # Get user data
    join_date = "N/A"
    try:
        member = await bot.get_chat_member(message.chat.id, target.id)
        join_date = datetime.fromtimestamp(member.joined_date).strftime("%Y-%m-%d") if member.joined_date else "Unknown"
    except:
        pass

    # Get group status
    status = "Member"
    if await bot.get_chat_member(message.chat.id, target.id):
        chat_member = await bot.get_chat_member(message.chat.id, target.id)
        if chat_member.status == "creator":
            status = "Group Owner 👑"
        elif chat_member.status == "administrator":
            status = "Admin ⚡"

    # Get warnings
    warn_data = await warns.find_one({"user_id": target.id, "chat_id": message.chat.id})
    warnings = warn_data.get("count", 0) if warn_data else 0

    # Build response
    response = (
        f"{emoji('📝')} **User Info:**\n"
        f"• Name: {target.mention}\n"
        f"• ID: `{target.id}`\n"
        f"• Joined: `{join_date}`\n"
        f"• Status: {status}\n"
        f"• Warnings: `{warnings}/3`"
    )
    
    await message.reply(response, disable_web_page_preview=True)
