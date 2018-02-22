#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Basic example for a bot that uses inline keyboards.
# This program is dedicated to the public domain under the CC0 license.
"""
import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
                          ConversationHandler, CallbackQueryHandler)

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)
lista = []

def create(bot,update):
    update.message.reply_text("")


def start(bot, update):
    user = update.message.text
    string = user[7:]
    keyboard = [[InlineKeyboardButton("Confirmar presença", callback_data='1',),
                 InlineKeyboardButton("Falta Justificada", callback_data='2')],
                ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text(text= string  , reply_markup=reply_markup)


def button(bot, update):
    query = update.callback_query
    username = update.callback_query.from_user['first_name'] + " " + update.callback_query.from_user['last_name']
    lista.append(username)
    bot.sendMessage(text="Presença confirmada: {} ".format(lista),
                          chat_id=query.message.chat_id)


def help(bot, update):
    update.message.reply_text("Use /start to test this bot.")


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    # Create the Updater and pass it your bot's token.
    updater = Updater("519608788:AAGg-pw9GFc_SMQvlGgxzMlEsGRsxxxyFZI")

    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CallbackQueryHandler(button))
    updater.dispatcher.add_handler(CommandHandler('help', help))
    updater.dispatcher.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT
    updater.idle()


if __name__ == '__main__':
    main()