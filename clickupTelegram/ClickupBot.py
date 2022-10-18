import config.config as config

from telegram.ext.updater import Updater
from telegram.update import Update
from telegram import (InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.messagehandler import MessageHandler
from telegram.ext import (ConversationHandler, ContextTypes, filters, CallbackQueryHandler, Filters)
import clickupApi.clickup_telegram_connector as infinity

updater = Updater(config.telegram_api,
                  use_context=True)


def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Welcome to the SPLUST Advanced modern solution to simplify working with Kanban ClickUp Dashboard")
    update.message.reply_text("To create new task simple send message")
    return help


def help(update: Update, context: CallbackContext):
    update.message.reply_text("To create new task simple send message")


def create_task(update: Update, context: CallbackContext):
    user_input = update.message.text
    keyboard = [
        [InlineKeyboardButton("Yes", callback_data="Yes"),
         InlineKeyboardButton("No", callback_data="No")]
    ]
    update.message.reply_text(f'Would you like to create task?\n\n{user_input}',
                              reply_markup=InlineKeyboardMarkup(keyboard))


def keyboard_callback_create_task(update: Update, context):
    query = update.callback_query
    # print('query:', query)

    print('query.data:', query.data)
    # query.answer(f'selected: {query.data}')
    if query.data == "Yes":
        print("1")
        description = str(query.message.text)[32:]
        infinity.create_task(description)

        query.edit_message_text("Task will be saved")

    elif query.data == "No":
        print("2")
        query.edit_message_text("task will be not saved")


if __name__ == "__main__":

    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CommandHandler('help', help))
    updater.dispatcher.add_handler(CallbackQueryHandler(keyboard_callback_create_task))
    updater.dispatcher.add_handler(MessageHandler(Filters.text, create_task))

    updater.start_polling()
    updater.idle()
