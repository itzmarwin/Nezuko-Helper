from pyrogram import filters
from nezukohelper.config import bot
from nezukohelper.utils.database import users
from nezukohelper.utils.helpers import emoji

@bot.on_message(filters.command("addsudo"))
async def add_sudo(_, message):
    # Owner check
    if message.from_user.id != bot.owner.id:
        return await message.reply(f"{emoji('🚫')} Only bot owner can use this!")

    # Get target user
    try:
        if message.reply_to_message:
            user = message.reply_to_message.from_user
        else:
            user_id = int(message.text.split()[1])
            user = await bot.get_users(user_id)
    except:
        return await message.reply(f"{emoji('⚠️')} Usage: /addsudo @username/reply")

    # Add to sudo
    await users.update_one(
        {"_id": user.id},
        {"$set": {"sudo": True}},
        upsert=True
    )
    await message.reply(f"{emoji('👑')} **{user.mention} added to sudo!**")

@bot.on_message(filters.command("rmsudo"))
async def remove_sudo(_, message):
    if message.from_user.id != bot.owner.id:
        return await message.reply(f"{emoji('🚫')} Owner-only command!")

    try:
        if message.reply_to_message:
            user = message.reply_to_message.from_user
        else:
            user_id = int(message.text.split()[1])
            user = await bot.get_users(user_id)
    except:
        return await message.reply(f"{emoji('⚠️')} Usage: /rmsudo @username/reply")

    # Remove sudo
    await users.update_one(
        {"_id": user.id},
        {"$unset": {"sudo": ""}}
    )
    await message.reply(f"{emoji('🗑')} **{user.mention} removed from sudo!**")

@bot.on_message(filters.command("sudolist"))
async def sudo_list(_, message):
    sudo_users = []
    async for user in users.find({"sudo": True}):
        try:
            user_obj = await bot.get_users(user["_id"])
            sudo_users.append(f"- {user_obj.mention} (`{user_obj.id}`)")
        except:
            pass
    
    text = f"{emoji('👑')} **Sudo Users:**\n" + "\n".join(sudo_users) if sudo_users else "No sudo users!"
    await message.reply(text)
