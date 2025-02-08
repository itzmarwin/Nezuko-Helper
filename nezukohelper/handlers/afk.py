from pyrogram import filters
from nezukohelper.config import bot
from nezukohelper.utils.database import afk
from nezukohelper.utils.helpers import emoji

@bot.on_message(filters.command("afk"))
async def set_afk(_, message):
    user = message.from_user
    reason = message.text.split(" ", 1)[1] if len(message.text.split()) > 1 else "Busy 🌸"
    
    await afk.update_one(
        {"_id": user.id},
        {"$set": {"reason": reason, "afk": True}},
        upsert=True
    )
    await message.reply(f"{emoji('🌸')} **{user.mention} is now AFK!**\nReason: {reason}")

@bot.on_message(filters.mentioned & ~filters.bot)
async def afk_mention(_, message):
    user_data = await afk.find_one({"_id": message.from_user.id})
    if user_data and user_data.get("afk"):
        await message.reply(f"{emoji('⚠️')} **This user is AFK!**\nReason: {user_data['reason']}")
        await afk.delete_one({"_id": message.from_user.id})
