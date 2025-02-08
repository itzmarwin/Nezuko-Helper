from pyrogram import filters
from nezukohelper.config import bot
from nezukohelper.utils.database import couples
from nezukohelper.utils.helpers import emoji
import random
import time

@bot.on_message(filters.command(["couple", "couples"]) & filters.group)
async def daily_couple(_, message):
    chat_id = message.chat.id

    # Check existing couple
    existing = await couples.find_one({"chat_id": chat_id})
    if existing and (time.time() - existing["timestamp"] < 86400):
        user1 = await bot.get_users(existing["user1"])
        user2 = await bot.get_users(existing["user2"])
        return await message.reply_photo(
            photo="https://telegra.ph/file/couple-template.jpg",  # Replace with your image
            caption=f"💑 **Today's Couple (Already Chosen):**\n{user1.mention} + {user2.mention} = ❤️"
        )

    # Get all members (exclude bots)
    members = [
        member.user.id 
        async for member in bot.get_chat_members(chat_id) 
        if not member.user.is_bot
    ]

    if len(members) < 2:
        return await message.reply(f"{emoji('⚠️')} Not enough members to pair!")

    # Select random pair
    user1_id, user2_id = random.sample(members, 2)
    user1 = await bot.get_users(user1_id)
    user2 = await bot.get_users(user2_id)

    # Save to DB
    await couples.update_one(
        {"chat_id": chat_id},
        {"$set": {"user1": user1_id, "user2": user2_id, "timestamp": time.time()}},
        upsert=True
    )

    # Send cute message
    await message.reply_photo(
        photo="https://telegra.ph/file/couple-template.jpg",
        caption=f"💘 **Couple of the Day:**\n{user1.mention} + {user2.mention} = ❤️\n*New pair at midnight!*"
  )
