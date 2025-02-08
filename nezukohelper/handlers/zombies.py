from pyrogram import filters
from nezukohelper.config import bot
from nezukohelper.utils.helpers import emoji

@bot.on_message(filters.command("zombies") & filters.group)
async def find_zombies(_, message):
    # Check admin rights
    admin = await bot.get_chat_member(message.chat.id, message.from_user.id)
    if not admin.privileges.can_restrict_members:
        return await message.reply(f"{emoji('⚠️')} Admin rights required!")

    zombies = []
    async for member in bot.get_chat_members(message.chat.id):
        if member.user.is_deleted:
            zombies.append(member.user.id)
    
    if not zombies:
        return await message.reply(f"{emoji('🌸')} No zombies found!")
    
    await message.reply(f"🧟 **Found {len(zombies)} deleted accounts!**\nUse `/zombies clean` to remove them.")

@bot.on_message(filters.command("zombies clean") & filters.group)
async def clean_zombies(_, message):
    admin = await bot.get_chat_member(message.chat.id, message.from_user.id)
    if not admin.privileges.can_restrict_members:
        return await message.reply(f"{emoji('⚠️')} Admin rights required!")

    zombies = []
    async for member in bot.get_chat_members(message.chat.id):
        if member.user.is_deleted:
            zombies.append(member.user.id)
    
    if not zombies:
        return await message.reply(f"{emoji('🌸')} No zombies to clean!")

    banned = 0
    for user_id in zombies:
        try:
            await bot.ban_chat_member(message.chat.id, user_id)
            banned += 1
        except Exception:
            pass
    
    await message.reply(f"{emoji('🧹')} **Cleaned {banned}/{len(zombies)} zombies!**")
