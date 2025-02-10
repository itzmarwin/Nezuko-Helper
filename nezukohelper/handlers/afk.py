from pyrogram import filters
from nezukohelper.config import bot
from nezukohelper.utils.database import get_collection
from nezukohelper.utils.helpers import emoji, log_error

afk_collection = get_collection("afk")  # Safe initialization

@bot.on_message(filters.command("afk"))
async def set_afk(_, message):
    try:
        user = message.from_user
        reason = message.text.split(" ", 1)[1] if len(message.text.split()) > 1 else "Busy 🌸"
        
        # Set AFK status
        await afk_collection.update_one(
            {"_id": user.id},
            {"$set": {"reason": reason, "afk": True}},
            upsert=True
        )
        await message.reply(f"{emoji('🌸')} **{user.mention} is now AFK!**\nReason: {reason}")
    
    except Exception as e:
        await log_error(e, "AFK Command")

@bot.on_message(filters.mentioned & ~filters.bot & ~filters.service)
async def afk_mention(client, message):
    try:
        # Check all mentioned users
        for user in message.entities:
            if user.user:
                afk_user = await afk_collection.find_one({"_id": user.user.id})
                if afk_user and afk_user.get("afk"):
                    await message.reply(
                        f"{emoji('⚠️')} **{afk_user.get('first_name', 'User')} is AFK!**\n"
                        f"Reason: {afk_user.get('reason', 'Not specified')}"
                    )
    except Exception as e:
        await log_error(e, "AFK Mention")

@bot.on_message(filters.private | (filters.group & ~filters.service))
async def afk_checker(client, message):
    try:
        user = message.from_user
        afk_data = await afk_collection.find_one({"_id": user.id})
        
        if afk_data and afk_data.get("afk"):
            # Remove AFK status
            await afk_collection.delete_one({"_id": user.id})
            await message.reply(f"{emoji('🎉')} Welcome back {user.mention}! Your AFK status is removed.")
    
    except Exception as e:
        await log_error(e, "AFK Checker")
