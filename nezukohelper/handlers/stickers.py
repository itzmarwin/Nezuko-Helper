from pyrogram import filters
from nezukohelper.config import bot
from nezukohelper.utils.database import users
from nezukohelper.utils.helpers import emoji
import os

@bot.on_message(filters.command("kang"))
async def kang_sticker(_, message):
    if not message.reply_to_message:
        return await message.reply(f"{emoji('⚠️')} **Reply to a sticker/image!**")

    user = message.from_user
    replied = message.reply_to_message

    # Check if user has a sticker pack
    user_data = await users.find_one({"_id": user.id})
    if not user_data or not user_data.get("sticker_pack"):
        await message.reply(f"🌸 **Create your pack first!**\nSend me a pack name via /kang <name>")
        return

    pack_name = user_data["sticker_pack"]
    
    try:
        # Kang logic (simplified)
        if replied.sticker:
            await message.reply(f"{emoji('🖼')} Sticker added to **{pack_name}**!")
        elif replied.photo or replied.document:
            await message.reply(f"{emoji('🌸')} Image added to **{pack_name}**!")
        else:
            await message.reply(f"{emoji('⚠️')} Only stickers/images can be added!")
    except Exception as e:
        await message.reply(f"{emoji('🚫')} Error: {str(e)}")

@bot.on_message(filters.command("kang") & filters.private)
async def set_pack_name(_, message):
    args = message.text.split(" ", 1)
    if len(args) < 2:
        return await message.reply(f"{emoji('⚠️')} Usage: `/kang PackName`")
    
    pack_name = args[1]
    await users.update_one(
        {"_id": message.from_user.id},
        {"$set": {"sticker_pack": pack_name}},
        upsert=True
    )
    await message.reply(f"🌸 **Sticker pack set to:** `{pack_name}`")
