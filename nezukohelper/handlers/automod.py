from pyrogram import filters
from nezukohelper.config import bot
from nezukohelper.utils.database import groups
from nezukohelper.utils.helpers import emoji

@bot.on_message(filters.group & ~filters.bot)
async def auto_delete_bad_words(_, message):
    # Check if AutoMod is enabled
    group_data = await groups.find_one({"chat_id": message.chat.id})
    if not group_data or not group_data.get("automod"):
        return

    # Get bad words list
    bad_words = group_data.get("bad_words", [])
    if not bad_words:
        return

    # Check message text
    text = message.text.lower() if message.text else ""
    if any(word in text for word in bad_words):
        await message.delete()
        await message.reply(
            f"{emoji('🚫')} **Message deleted!**\n"
            f"{message.from_user.mention}, avoid using restricted words."
        )

@bot.on_message(filters.command("addbadword") & filters.group)
async def add_bad_word(_, message):
    # Admin check
    admin = await bot.get_chat_member(message.chat.id, message.from_user.id)
    if not admin.privileges.can_delete_messages:
        return await message.reply(f"{emoji('⚠️')} Admin rights required!")

    args = message.text.split(" ", 1)
    if len(args) < 2:
        return await message.reply(f"{emoji('⚠️')} Usage: /addbadword <word>")

    word = args[1].lower()
    await groups.update_one(
        {"chat_id": message.chat.id},
        {"$addToSet": {"bad_words": word}},
        upsert=True
    )
    await message.reply(f"{emoji('✅')} Added `{word}` to restricted list!")

@bot.on_message(filters.command("rmbadword") & filters.group)
async def remove_bad_word(_, message):
    admin = await bot.get_chat_member(message.chat.id, message.from_user.id)
    if not admin.privileges.can_delete_messages:
        return await message.reply(f"{emoji('⚠️')} Admin rights required!")

    args = message.text.split(" ", 1)
    if len(args) < 2:
        return await message.reply(f"{emoji('⚠️')} Usage: /rmbadword <word>")

    word = args[1].lower()
    await groups.update_one(
        {"chat_id": message.chat.id},
        {"$pull": {"bad_words": word}}
    )
    await message.reply(f"{emoji('🗑')} Removed `{word}` from restricted list!")

@bot.on_message(filters.command("badwords") & filters.group)
async def list_bad_words(_, message):
    group_data = await groups.find_one({"chat_id": message.chat.id})
    words = group_data.get("bad_words", []) if group_data else []
    await message.reply(
        f"{emoji('📜')} **Restricted Words:**\n" + "\n".join([f"- `{w}`" for w in words])
        if words else f"{emoji('🌸')} No bad words set!"
  )
