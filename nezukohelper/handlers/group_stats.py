from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
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
async def group_stats(_, message: Message):
    if message.chat.type not in ["group", "supergroup"]:
        return await message.reply("❌ This command works only in groups!")
    
    await message.reply(
        f"{emoji('📊')} **Group Statistics**\nChoose a category:",
        reply_markup=STATS_BUTTONS
    )

@bot.on_callback_query(filters.regex(r"today_stats|alltime_stats"))
async def show_stats(client, query):
    try:
        chat_id = query.message.chat.id
        timeframe = "today" if "today" in query.data else "alltime"

        pipeline = []
        if timeframe == "today":
            pipeline.append({"$match": {
                "chat_id": chat_id,
                "timestamp": {"$gte": time.time() - 86400}
            }})
        else:
            pipeline.append({"$match": {"chat_id": chat_id}})
        
        pipeline.extend([
            {"$group": {"_id": "$user_id", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}},
            {"$limit": 10}
        ])

        top_users = []
        async for user_data in messages.aggregate(pipeline):
            try:
                user = await client.get_users(user_data["_id"])
                top_users.append(f"• {user.mention} » **{user_data['count']}**")
            except Exception as e:
                print(f"User Fetch Error: {e}")
        
        text = f"{emoji('🏆')} **Top 10 {'Today' if timeframe == 'today' else 'All-Time'}**\n\n"
        text += "\n".join(top_users) if top_users else "No data yet!"
        await query.message.edit(text, reply_markup=STATS_BUTTONS)
    
    except Exception as e:
        await query.answer(f"❌ Error: {str(e)}", show_alert=True)

@bot.on_callback_query(filters.regex("close_stats"))
async def close_stats(_, query):
    try:
        await query.message.delete()
    except:
        await query.answer("⚠️ Message already deleted!")

@bot.on_message(
    (filters.group) & 
    (~filters.service) & 
    (~filters.command()) &  # ✅ सही syntax (commands को exclude करें)
    (~filters.edited)
)
async def track_message(_, message: Message):
    if not message.from_user:
        return
    
    try:
        await messages.insert_one({
            "user_id": message.from_user.id,
            "chat_id": message.chat.id,
            "timestamp": time.time()
        })
    except Exception as e:
        print(f"Database Insert Error: {e}")
