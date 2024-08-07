#!/usr/bin/env python
# pylint: disable=unused-argument
# This program is dedicated to the public domain under the CC0 license.

"""
Basic example for a bot that uses inline keyboards. For an in-depth explanation, check out
 https://github.com/python-telegram-bot/python-telegram-bot/wiki/InlineKeyboard-Example.
"""
import logging

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, Update, WebAppInfo, LoginUrl,CallbackGame
from telegram.ext import Application, CallbackQueryHandler, CommandHandler, ContextTypes, MessageHandler, filters

TOKEN = "7096248383:AAGpXeaj0a2UglSAckDy6JAjelETMAjiRSA"
GAME_SHORT_GAME = "camel"
# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends a message with three inline buttons attached."""
# 创建按钮
    button1 = KeyboardButton(text='🎮Start Playing')
    button2 = KeyboardButton('🐫Game Introduction')
    

    # 创建键盘
    keyboard = [[button1],[button2, KeyboardButton('☎️Help Center')]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    # 发送消息并附带键盘
    await update.message.reply_text('Welcome on board!', reply_markup=reply_markup)
    

async def playgame(update:Update,context:ContextTypes.DEFAULT_TYPE):
    login_url = LoginUrl(url='https://game.ohayoaptos.com/camel/tg_login')
    
    keyboard = [
        [InlineKeyboardButton(text="Play Yalla Jamel", callback_game=CallbackGame(), login_url=login_url)]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await context.bot.send_game(chat_id=update.effective_chat.id, game_short_name = GAME_SHORT_GAME, reply_markup = reply_markup)

### 外部链接 ###
async def playgameinbrower(update:Update,context:ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton(text="Play Yalla Jamel", url="https://game.ohayoaptos.com/camel_app/")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await context.bot.send_photo(chat_id=update.effective_chat.id, 
                                photo="https://game.ohayoaptos.com/camel_app/vfdd.jpg",
                                caption="There are 7 slots at the bottom of the game, players only need to place 3 pieces of the same bricks into the slots and they will compete. Brick cannot be moved if there is not one brick above it.", 
                                reply_markup=reply_markup)

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Parses the CallbackQuery and updates the message text."""
    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    cqid = update.callback_query.id
    query = update.callback_query
    #await query.answer()
    logger.info(query.game_short_name)
    # if query.inline_message_id
    if query.game_short_name != None :
        await context.bot.answerCallbackQuery(callback_query_id=cqid, url='https://game.ohayoaptos.com/camel_app/')    

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Displays info on how to use the bot."""
    await update.message.reply_text("Use /game to start playing.")


def main() -> None:
    """Run the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(TOKEN).build()

    gamelink_handler = MessageHandler((filters.Regex('🐫Game Introduction')),playgame)
    gamelink_handler = MessageHandler((filters.Regex('🎮Start Playing')),playgame)
    game_handler = CommandHandler('game',playgame)

    application.add_handler(gamelink_handler)
    application.add_handler(game_handler)
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button))
    application.add_handler(CommandHandler("help", help_command))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()