from pyrogram import filters
from nezukohelper.config import bot
from nezukohelper.utils.database import groups
from nezukohelper.utils.helpers import emoji
import asyncio

@bot.on_message(filters.command("tagall") & filters.group)
async def tag_all_members(_, message):
    # Check admin rights
    admin = await bot.get_chat_member(message.chat.id, message.from_user.id)
    if not admin.privileges.can_mention:
        return await message.reply(f"{emoji('⚠️')} Admin rights required!")

    # Get custom message
    args = message.text.split(" ", 1)
    custom_msg = args[1] if len(args) > 1 else "Hey everyone! 🌸"

    # Fetch all members
    mentions = []
    async for member in bot.get_chat_members(message.chat.id):
        if member.user.username:
            mentions.append(f"@{member.user.username}")
        else:
            mentions.append(f"[{member.user.first_name}](tg://user?id={member.user.id})")

    # Send in chunks (50 per message)
    for i in range(0, len(mentions), 50):
        chunk = mentions[i:i+50]
        await message.reply(f"{custom_msg}\n\n" + "\n".join(chunk))
        await asyncio.sleep(1)  # Avoid flood

@bot.on_message(filters.command("cancel") & filters.group)
async def cancel_tagall(_, message):
    # Implementation would require tracking active tagall operations
    await message.reply(f"{emoji('⚠️')} No active tagall to cancel!")
