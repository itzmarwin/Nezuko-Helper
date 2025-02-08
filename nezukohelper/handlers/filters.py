from pyrogram import filters
from nezukohelper.config import bot
from nezukohelper.utils.database import filters_db
from nezukohelper.utils.helpers import emoji

@bot.on_message(filters.command("filter") & filters.group)
async def add_filter(_, message):
    # Check admin rights
    admin = await bot.get_chat_member(message.chat.id, message.from_user.id)
    if not admin.privileges.can_change_info:
        return await message.reply(f"{emoji('⚠️')} Admin rights required!")

    args = message.text.split(" ", 2)
    if len(args) < 3:
        return await message.reply(f"{emoji('⚠️')} Usage: /filter <keyword> <reply>")

    keyword = args[1].lower()
    reply = args[2]

    await filters_db.update_one(
        {"chat_id": message.chat.id, "keyword": keyword},
        {"$set": {"reply": reply}},
        upsert=True
    )
    await message.reply(f"{emoji('🌸')} Added filter for: `{keyword}`")

@bot.on_message(filters.group & ~filters.bot)
async def filter_trigger(_, message):
    text = message.text.lower() if message.text else ""
    if not text:
        return

    async for flt in filters_db.find({"chat_id": message.chat.id}):
        if flt["keyword"] in text:
            await message.reply(flt["reply"])
            break

@bot.on_message(filters.command("filters") & filters.group)
async def list_filters(_, message):
    filters_list = []
    async for flt in filters_db.find({"chat_id": message.chat.id}):
        filters_list.append(f"- `{flt['keyword']}`")
    
    text = f"{emoji('📜')} **Active Filters:**\n" + "\n".join(filters_list) if filters_list else "No filters set!"
    await message.reply(text)

@bot.on_message(filters.command("stop") & filters.group)
async def remove_filter(_, message):
    args = message.text.split(" ", 1)
    if len(args) < 2:
        return await message.reply(f"{emoji('⚠️')} Usage: /stop <keyword>")

    keyword = args[1].lower()
    result = await filters_db.delete_one({"chat_id": message.chat.id, "keyword": keyword})
    
    if result.deleted_count:
        await message.reply(f"{emoji('🗑')} Deleted filter: `{keyword}`")
    else:
        await message.reply(f"{emoji('⚠️')} Filter not found!")
