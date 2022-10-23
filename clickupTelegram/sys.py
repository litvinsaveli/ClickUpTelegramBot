import os
import sys

sys.path.insert(1, os.path.dirname(os.path.abspath(os.path.join(sys.argv[0], os.pardir))))

import config.config as config
from telegram.ext.updater import Updater
from telegram.update import Update
from telegram import (InlineKeyboardMarkup, InlineKeyboardButton, ForceReply)
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.callbackqueryhandler import CallbackQueryHandler
from telegram.ext import (ConversationHandler, CallbackQueryHandler, Filters)

import clickupApi.clickup_telegram_connector as infinity
import DB_connector as DB
import helpers.Exceptions as CustomException
import helpers.bot_functions as BF

updater = Updater(config.telegram_api,
                  use_context=True)


def start(update: Updater, context: CallbackContext):
    diction = {"SPLUST": 4733034, "DailyDigest": 30326153, "userflowoverwodw1": 1, "userflow2": 2, "userflow3": 3, "userflow5":5,
               "userflow4": 4}

    # dynamic keyboard prototype
    insider = [InlineKeyboardButton(f"{key}", callback_data=f"{value}") for key, value in diction.items()]
    button = [insider[i:i + 2] for i in range(0, len(insider), 2)]

    print(button)
    print(len(button))
    print(len(button[0]))
    markup = InlineKeyboardMarkup(button)
    update.message.reply_text("Callback test", reply_markup=markup)


updater.dispatcher.add_handler(CommandHandler("start", start), group=1)
print("Started ...")
updater.start_polling()
updater.idle()
