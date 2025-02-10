from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from nezukohelper.config import bot
from nezukohelper.utils.helpers import emoji
import logging

logger = logging.getLogger(__name__)

# ========== START MENU ==========
START_TEXT = (
    f"{emoji('🌸')} **Konnichiwa!** I'm **Nezuko Helper**~\n"
    "I can manage groups, play games, and keep things fun!\n"
    "Use the buttons below to explore my commands. 💖"
)

START_BUTTONS = InlineKeyboardMarkup([
    [InlineKeyboardButton("➕ Add to Group", url="https://t.me/nezukohelperbot?startgroup=true")],
    [
        InlineKeyboardButton("📜 Commands", callback_data="help_menu"),
        InlineKeyboardButton("👑 Owner", callback_data="owner_info")
    ],
    [
        InlineKeyboardButton("💬 Support", url="https://t.me/Anime_group_chat_en"),
        InlineKeyboardButton("📢 Channel", url="https://t.me/Samurais_network")
    ]
])

# ========== HELP MENU ==========
HELP_BUTTONS = InlineKeyboardMarkup([
    [
        InlineKeyboardButton("🛠️ Moderation", callback_data="help_mod"),
        InlineKeyboardButton("🎮 Games", callback_data="help_games")
    ],
    [
        InlineKeyboardButton("✨ Utilities", callback_data="help_utils"),
        InlineKeyboardButton("🔙 Back", callback_data="back_start")
    ]
])

HELP_TEXTS = {
    "help_mod": (
        f"{emoji('⚔️')} **Moderation Commands**\n\n"
        "• /ban - Ban a user\n"
        "• /warn - Warn users (3 warns = ban)\n"
        "• /zombies - Clean deleted accounts\n"
        "• /gban - Globally ban a user"
    ),
    "help_games": (
        f"{emoji('🎲')} **Games**\n\n"
        "• /dice - Roll a dice\n"
        "• /dart - Throw a dart\n"
        "• /basket - Play basketball\n"
        "• /couple - Daily couple pairing"
    ),
    "help_utils": (
        f"{emoji('🔧')} **Utilities**\n\n"
        "• /afk - Set AFK status\n"
        "• /kang - Create sticker packs\n"
        "• /info - Get user details\n"
        "• /gstat - Group leaderboard"
    )
}

@bot.on_message(filters.command("start"))
async def start_cmd(client, message):
    try:
        await message.reply_photo(
            photo="https://telegra.ph/file/6b1c56f02fcad5ce73708-906cca241fa16c959b.jpg",
            caption=START_TEXT,
            reply_markup=START_BUTTONS
        )
    except Exception as e:
        logger.error(f"Start command error: {str(e)}")
        await message.reply("❌ Failed to load start menu!")

@bot.on_callback_query(filters.regex(r"help_|back_start|owner_info"))
async def handle_buttons(client, query):
    try:
        data = query.data
        
        if data == "help_menu":
            await query.message.edit(
                "📚 **Command Categories**\nChoose a category:",
                reply_markup=HELP_BUTTONS
            )
        elif data == "owner_info":
            await query.answer("👑 Owner: @Itz_Marv1n\nDM for support!", show_alert=True)
            return  # No message edit needed
        elif data.startswith("help_"):
            if data not in HELP_TEXTS:
                return await query.answer("⚠️ Invalid menu!", show_alert=True)
                
            await query.message.edit(
                HELP_TEXTS[data],
                reply_markup=HELP_BUTTONS
            )
        elif data == "back_start":
            await query.message.edit(
                START_TEXT,
                reply_markup=START_BUTTONS
            )
        
        await query.answer()
    except Exception as e:
        logger.error(f"Button handler error: {str(e)}")
        await query.answer("❌ Something went wrong!", show_alert=True)
