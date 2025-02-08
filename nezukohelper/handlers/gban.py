from pyrogram import filters
from nezukohelper.config import bot
from nezukohelper.utils.database import gbans, groups
from nezukohelper.utils.helpers import emoji
import asyncio

@bot.on_message(filters.command("gban"))
async def global_ban(_, message):
    # Check sudo/owner access
    user_data = await users.find_one({"_id": message.from_user.id})
    if not user_data or not user_data.get("sudo"):
        return await message.reply(f"{emoji('🚫')} Owner/Sudo only!")

    # Get target user
    try:
        if message.reply_to_message:
            target = message.reply_to_message.from_user
        else:
            args = message.text.split()
            if len(args) < 2:
                return await message.reply(f"{emoji('⚠️')} Usage: /gban @user/id")
            target = await bot.get_users(args[1])
    except:
        return await message.reply(f"{emoji('🚫')} Invalid user!")

    # Check if already GBanned
    if await gbans.find_one({"user_id": target.id}):
        return await message.reply(f"{emoji('⚠️')} User already GBanned!")

    # Ban in all groups
    processing = await message.reply(f"{emoji('⚡')} Initiating global ban on {target.mention}...")
    banned_chats = 0
    total_chats = 0

    async for group in groups.find({}):
        total_chats += 1
        try:
            await bot.ban_chat_member(group["chat_id"], target.id)
            banned_chats += 1
        except Exception as e:
            pass
        await asyncio.sleep(0.5)  # Avoid flood

    # Save to GBans list
    await gbans.update_one(
        {"user_id": target.id},
        {"$set": {"banned_by": message.from_user.id, "chat_count": banned_chats}},
        upsert=True
    )

    # Send report
    await processing.edit(
        f"{emoji('🌍')} **Globally Banned!**\n"
        f"• User: {target.mention}\n"
        f"• Banned in: {banned_chats}/{total_chats} groups\n"
        f"• Banned by: {message.from_user.mention}"
    )

@bot.on_chat_member_updated()
async def auto_ban_gbanned(_, chat_member):
    if chat_member.new_chat_member:
        user_id = chat_member.new_chat_member.user.id
        if await gbans.find_one({"user_id": user_id}):
            try:
                await bot.ban_chat_member(chat_member.chat.id, user_id)
            except:
                pass
