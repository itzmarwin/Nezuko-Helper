from pyrogram import filters
from nezukohelper.config import bot
from nezukohelper.utils.database import warns
from nezukohelper.utils.helpers import emoji

@bot.on_message(filters.command("warn") & filters.group)
async def warn_user(_, message):
    # Check admin rights
    admin = await bot.get_chat_member(message.chat.id, message.from_user.id)
    if not admin.privileges.can_restrict_members:
        return await message.reply(f"{emoji('⚠️')} Admin rights required!")

    # Get target user
    if not message.reply_to_message:
        return await message.reply(f"{emoji('⚠️')} Reply to a user!")
    target = message.reply_to_message.from_user

    # Update warnings
    await warns.update_one(
        {"user_id": target.id, "chat_id": message.chat.id},
        {"$inc": {"count": 1}},
        upsert=True
    )

    # Check if 3+ warnings
    warn_data = await warns.find_one({"user_id": target.id, "chat_id": message.chat.id})
    current_warnings = warn_data.get("count", 0) if warn_data else 0

    if current_warnings >= 3:
        await bot.ban_chat_member(message.chat.id, target.id)
        await message.reply(
            f"{emoji('🚫')} **Banned {target.mention}**\n"
            f"Reason: Reached 3/3 warnings!"
        )
        await warns.delete_one({"user_id": target.id, "chat_id": message.chat.id})
    else:
        await message.reply(
            f"{emoji('⚠️')} {target.mention} warned!\n"
            f"Warnings: {current_warnings}/3"
        )

@bot.on_message(filters.command(["warnings", "warnlist"]) & filters.group)
async def check_warnings(_, message):
    if not message.reply_to_message:
        return await message.reply(f"{emoji('⚠️')} Reply to a user!")
    target = message.reply_to_message.from_user

    warn_data = await warns.find_one({"user_id": target.id, "chat_id": message.chat.id})
    count = warn_data.get("count", 0) if warn_data else 0
    await message.reply(f"{emoji('📜')} {target.mention} has **{count}/3** warnings!")

@bot.on_message(filters.command("resetwarns") & filters.group)
async def reset_warnings(_, message):
    if not message.reply_to_message:
        return await message.reply(f"{emoji('⚠️')} Reply to a user!")
    target = message.reply_to_message.from_user

    await warns.delete_one({"user_id": target.id, "chat_id": message.chat.id})
    await message.reply(f"{emoji('🌸')} Warnings reset for {target.mention}!")
