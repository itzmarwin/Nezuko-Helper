from pyrogram import filters
from pyrogram.types import Dice, Message
from nezukohelper.config import bot
from nezukohelper.utils.helpers import emoji

GAMES = {
    "dice": "🎲",
    "dart": "🎯",
    "basket": "🏀",
    "bowling": "🎳",
    "slot": "🎰"
}

@bot.on_message(filters.command(list(GAMES.keys())))
async def play_game(_, message: Message):
    game = message.command[0]
    emoji = GAMES[game]
    
    # Send game animation
    msg = await message.reply_dice(emoji=emoji)
    
    # Optional: Add result message
    await message.reply(
        f"{emoji} **{message.from_user.mention} played {game}!**\n"
        f"Result: **{msg.dice.value}**"
    )
