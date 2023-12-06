#!/usr/bin/env python
# pylint: disable=unused-argument
# This program is dedicated to the public domain under the CC0 license.

"""
Simple example of a Telegram WebApp which displays a color picker.
The static website for this website is hosted by the PTB team for your convenience.
Currently only showcases starting the WebApp via a KeyboardButton, as all other methods would
require a bot token.
"""
import json
import logging
import yaml
import os

from telegram import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, Update, WebAppInfo, InlineKeyboardButton, InlineKeyboardMarkup, InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters, CallbackQueryHandler, InlineQueryHandler

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

botToken = ""
twaUrl = ""
turnupUrl = ""

logger = logging.getLogger(__name__)

inlinePlayGameButton = None
inlineCallbackMenuButton = None
inlineJumpToChatRoom = None
inlineJumpToAnnouncementChannel = None
inlineShareButton = None

# Define a `/start` command handler.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        text="Welcome to TURNUP for Telegram",
        parse_mode="Html",
    )
    inlineButtonRow = []
    inlineButtonRow.append(inlinePlayGameButton)
    inlineButtonRow.append(inlineCallbackMenuButton)
    await update.message.reply_photo(
        photo="https://tg-dev.badass.xyz/default-assets/welcome_image.jpg",
        caption="Play TURNUP Trivia\nEarn $100 Rewards Everyday",
        reply_markup=InlineKeyboardMarkup.from_row(
            inlineButtonRow
        ),
    )

async def inlineButtonCallback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    if query.data == "/menu" :
        inlineButtonRow = [[],[]]
        inlineButtonRow[0].append(inlinePlayGameButton)
        inlineButtonRow[0].append(inlineJumpToChatRoom)
        inlineButtonRow[1].append(inlineJumpToAnnouncementChannel)
        inlineButtonRow[1].append(inlineShareButton)
        await query.get_bot().send_photo(
            chat_id=query.message.chat.id,
            photo="https://tg-dev.badass.xyz/default-assets/go_turnup_image.jpg",
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=inlineButtonRow
            ),
        )
    await query.answer()

async def inlineQueryFunc(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global twaUrl
    query = update.inline_query
    result = []
    result.append(InlineQueryResultArticle(
        id=query.id,
        title="Go Turnup",
        input_message_content=InputTextMessageContent(twaUrl)
    ))
    await query.answer(
        result
    )

def loadConfig() -> None:
    global botToken
    global twaUrl
    global turnupUrl
    filename = os.path.join(os.path.dirname(__file__),'config.yaml').replace("\\","/")
    with open(filename,'r') as f:
        data = yaml.full_load(f.read())
        botToken = data['botToken']
        twaUrl = data['twaUrl']
        turnupUrl = data['turnupUrl']

def initButton() -> None:
    global turnupUrl
    global inlinePlayGameButton
    inlinePlayGameButton = InlineKeyboardButton(
            text="Go Turnup",
            web_app=WebAppInfo(url=turnupUrl),
        )
    global inlineCallbackMenuButton
    inlineCallbackMenuButton = InlineKeyboardButton(
            text="Menu",
            callback_data="/menu",
        )
    global inlineJumpToChatRoom
    inlineJumpToChatRoom = InlineKeyboardButton(
            text="Chat",
            url="https://t.me/+pc0UVo5LbhQ1NDQ9",
        )
    global inlineJumpToAnnouncementChannel
    inlineJumpToAnnouncementChannel = InlineKeyboardButton(
            text="Announcement",
            url="https://t.me/+Glz9IcORjX80OTg1",
        )
    global inlineShareButton
    inlineShareButton = InlineKeyboardButton(
            text="Share",
            switch_inline_query="",
        )

def main() -> None:
    """Start the bot."""
    loadConfig()
    initButton()
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(botToken).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(inlineButtonCallback))
    application.add_handler(InlineQueryHandler(inlineQueryFunc))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
