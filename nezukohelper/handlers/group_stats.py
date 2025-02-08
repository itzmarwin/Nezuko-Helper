from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from nezukohelper.config import bot
from nezukohelper.utils.database import messages
from nezukohelper.utils.helpers import emoji
import time

# ========== LEADERBOARD BUTTONS ==========
STATS_BUTTONS = InlineKeyboardMarkup([
    [InlineKeyboardButton("📅 Today", callback_data="today_stats")],
    [InlineKeyboardButton("🏆 All-Time", callback_data="alltime_stats")],
    [InlineKeyboardButton("❌ Close", callback_data="close_stats")]
])

@bot.on_message(filters.command("gstat"))
async def group_stats(_, message):
    await message.reply(
        f"{emoji('📊')} **Group Statistics**\nChoose a category:",
        reply_markup=STATS_BUTTONS
    )

@bot.on_callback_query(filters.regex("today_stats|alltime_stats"))
async def show_stats(_, query):
    chat_id = query.message.chat.id
    timeframe = "today" if "today" in query.data else "alltime"

    # Build aggregation pipeline
    pipeline = []
    if timeframe == "today":
        pipeline.append({"$match": {"timestamp": {"$gte": time.time() - 86400}}})
    
    pipeline.extend([
        {"$group": {"_id": "$user_id", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 10}
    ])

    # Fetch top users
    top_users = []
    async for user in messages.aggregate(pipeline):
        try:
            user_obj = await bot.get_users(user["_id"])
            top_users.append(f"• {user_obj.mention} » **{user['count']}** messages")
        except:
            pass

    # Build response
    text = f"{emoji('🏆')} **Top 10 {'Today' if timeframe == 'today' else 'All-Time'}**\n\n"
    text += "\n".join(top_users) if top_users else "No data yet!"
    await query.message.edit(text, reply_markup=STATS_BUTTONS)

@bot.on_callback_query(filters.regex("close_stats"))
async def close_stats(_, query):
    await query.message.delete()

@bot.on_message(filters.group & ~filters.service & ~filters.command)
async def track_message(_, message):
    # Save message to DB
    await messages.insert_one({
        "user_id": message.from_user.id,
        "chat_id": message.chat.id,
        "timestamp": time.time()
    })
