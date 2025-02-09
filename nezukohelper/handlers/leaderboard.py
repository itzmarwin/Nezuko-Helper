from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from nezukohelper.config import bot
from nezukohelper.utils.database import messages
from nezukohelper.utils.helpers import emoji
import time
import asyncio

# ========== AUTO DAILY RESET ==========
async def reset_daily_stats():
    while True:
        now = time.time()
        next_reset = now - (now % 86400) + 86400  # Next midnight UTC
        await asyncio.sleep(next_reset - now)
        await messages.delete_many({"scope": "daily"})

# Start reset loop
bot.loop.create_task(reset_daily_stats())

# ========== LEADERBOARD MENU ==========
LB_BUTTONS = InlineKeyboardMarkup([
    [InlineKeyboardButton("📅 Today", callback_data="lb_today"),
     InlineKeyboardButton("🏆 All-Time", callback_data="lb_alltime")],
    [InlineKeyboardButton("❌ Close", callback_data="lb_close")]
])

@bot.on_message(filters.command("gstat"))
async def leaderboard_menu(_, message):
    await message.reply(
        f"{emoji('🏆')} **Leaderboard**\nChoose a category:",
        reply_markup=LB_BUTTONS
    )

# ========== LEADERBOARD HANDLERS ==========
@bot.on_callback_query(filters.regex("lb_today|lb_alltime"))
async def show_leaderboard(_, query):
    timeframe = "daily" if "today" in query.data else "alltime"
    
    pipeline = []
    if timeframe == "daily":
        pipeline.append({"$match": {"timestamp": {"$gte": time.time() - 86400}}})
    
    pipeline.extend([
        {"$group": {"_id": "$user_id", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 10}
    ])

    top_users = []
    async for user in messages.aggregate(pipeline):
        try:
            user_obj = await bot.get_users(user["_id"])
            top_users.append(f"• {user_obj.mention} » **{user['count']}** messages")
        except:
            pass

    text = f"{emoji('🏅')} **Top 10 {'Today' if timeframe == 'daily' else 'All-Time'}**\n\n"
    text += "\n".join(top_users) if top_users else "No data yet!"
    await query.message.edit(text, reply_markup=LB_BUTTONS)

@bot.on_callback_query(filters.regex("lb_close"))
async def close_leaderboard(_, query):
    await query.message.delete()

# ========== MESSAGE TRACKING ==========
@bot.on_message(filters.group & ~filters.service & ~filters.command)
async def track_activity(_, message):
    await messages.insert_one({
        "user_id": message.from_user.id,
        "chat_id": message.chat.id,
        "timestamp": time.time(),
        "scope": "alltime"
    })
    await messages.insert_one({
        "user_id": message.from_user.id,
        "chat_id": message.chat.id,
        "timestamp": time.time(),
        "scope": "daily"
    })
