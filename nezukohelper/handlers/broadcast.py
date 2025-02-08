from pyrogram import filters
from nezukohelper.config import bot
from nezukohelper.utils.database import users, groups, broadcasts
from nezukohelper.utils.helpers import emoji
import asyncio
import time

# Broadcast lock to prevent multiple broadcasts
BROADCAST_LOCK = asyncio.Lock()

@bot.on_message(filters.command("broadcast") & filters.private)
async def broadcast_message(_, message):
    # Check sudo/owner
    user_data = await users.find_one({"_id": message.from_user.id})
    if not user_data or not user_data.get("sudo"):
        return await message.reply(f"{emoji('🚫')} Owner/Sudo only!")

    # Get broadcast content
    if not message.reply_to_message:
        args = message.text.split(" ", 1)
        if len(args) < 2:
            return await message.reply(f"{emoji('⚠️')} Usage: /broadcast <message>")
        content = args[1]
        is_media = False
    else:
        content = message.reply_to_message
        is_media = True

    # Start broadcast
    processing = await message.reply(f"{emoji('📡')} **Broadcast Started...**")
    total = success = failed = 0

    async with BROADCAST_LOCK:
        # Send to all users
        async for user in users.find({}):
            try:
                if is_media:
                    await content.copy(user["_id"])
                else:
                    await bot.send_message(user["_id"], content)
                success += 1
            except Exception as e:
                failed += 1
            total += 1
            if total % 20 == 0:
                await processing.edit(f"**Progress:** {total} users | ✅ {success} | ❌ {failed}")

        # Send to all groups
        async for group in groups.find({}):
            try:
                if is_media:
                    await content.copy(group["chat_id"])
                else:
                    await bot.send_message(group["chat_id"], content)
                success += 1
            except:
                failed += 1
            total += 1
            if total % 20 == 0:
                await processing.edit(f"**Progress:** {total} chats | ✅ {success} | ❌ {failed}")

        # Save broadcast log
        await broadcasts.insert_one({
            "by": message.from_user.id,
            "timestamp": time.time(),
            "success": success,
            "failed": failed,
            "total": total
        })

        # Final report
        await processing.edit(
            f"{emoji('✅')} **Broadcast Completed!**\n\n"
            f"• Total: `{total}`\n"
            f"• Success: `{success}`\n"
            f"• Failed: `{failed}`"
        )
