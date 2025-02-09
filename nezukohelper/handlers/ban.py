from pyrogram import filters
from nezukohelper.config import bot
from nezukohelper.utils.database import groups
from nezukohelper.utils.helpers import emoji

@bot.on_message(filters.command("ban") & filters.group)
async def ban_user(_, message):
    # Check admin rights
    admin = await bot.get_chat_member(message.chat.id, message.from_user.id)
    if not admin.privileges.can_restrict_members:
        return await message.reply(f"{emoji('⚠️')} You need admin rights to ban users!")

    # Get target user
    try:
        if message.reply_to_message:
            target = message.reply_to_message.from_user
        else:
            args = message.text.split()
            if len(args) < 2:
                return await message.reply(f"{emoji('🌸')} Usage: `/ban @username/reply`")
            target = await bot.get_users(args[1])
    except Exception as e:
        return await message.reply(f"{emoji('🚫')} Error: {str(e)}")

    # Ban user and send confirmation
    try:
        await bot.ban_chat_member(message.chat.id, target.id)
        reason = " ".join(args[2:]) if len(args) > 2 else "No reason specified"
        await message.reply(
            f"{emoji('🚷')} **{target.mention} banned!**\n"
            f"Reason: {reason}\n"
            f"By: {message.from_user.mention}"
        )
    except Exception as e:
        await message.reply(f"{emoji('⚠️')} Failed to ban user: {str(e)}")
