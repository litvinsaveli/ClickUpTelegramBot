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
from telegram.ext import (ConversationHandler, CallbackQueryHandler, Filters, DispatcherHandlerStop, handler)

import clickupApi.clickup_telegram_connector as infinity
import DB_connector as DB
import helpers.Exceptions as CustomException

updater = Updater(config.telegram_api,
                  use_context=True)


def backlog_checker(update: Updater, context: CallbackContext):
    """
    Authorization hidden layer

    Status == 1 > user has committed full registration process
    Status == 0 > user does not complete registration

    Hypothesis 1: after registration on ClickUp user have no available spaces
    Research: Registration creates at least 1 space

    Hypothesis 2: after Hypothesis 1 do deleting a board
    Research: Possible. Need to prevent such case ToDo
    """
    print("backlog checker")
    try:
        if context.user_data["status"]:
            print("1")
            if context.user_data["status"] == 1:
                print("2")
                if not context.user_data["active_list"]:
                    context.user_data["active_list"] = DB.get_active_userspace(context.user_data["user_id"])

                if not context.user_data["api"]:
                    context.user_data["api"] = DB.get_user_api(context.user_data["user_id"])


            elif context.user_data["status"] == 0:
                print("why nothing raised idiot")
                raise DispatcherHandlerStop(MessageHandler(Filters.text, message_handler))

    except KeyError:
        """
        Reboot handler
        """
        context.user_data["user_id"] = update.message.chat_id
        context.user_data["status"] = DB.check_is_user_registed(context.user_data["user_id"])

        if context.user_data["status"] == 1:
            context.user_data["boards"] = DB.get_list_workspaces(context.user_data["user_id"])
            context.user_data["active_list"] = DB.get_active_userspace(context.user_data["user_id"])
            print(context.user_data["active_list"])

            updater.dispatcher.add_handler(MessageHandler(Filters.text, message_handler), group=3)

            """Its enough at this stage"""

        elif context.user_data["status"] == 0:
            pass


def start(update: Updater, context: CallbackContext):
    update.message.reply_text(
        "Welcome to the SPLUST Advanced modern solution to simplify working with Kanban ClickUp Dashboard"
    )
    if context.user_data["status"] == 0:
        update.message.reply_text(
            "To start working with SPLUST setup your api key /set_api"
        )
    if context.user_data["status"] == 1:
        pass


def set_api(update: Updater, context: CallbackContext):
    """
    this function could be handleable only when api key is not set up
    """
    if context.user_data["status"] == 0:
        update.message.reply_text(
            "We need your api key to give you access to your boards and tasks. For that please follow instruction:\n"
            "1. login to your clickup using web version.\n"
            "2. click left lower corner on your boards as well your profile\n"
            "3. under your profile click My Settings\n"
            "4. in the left side bar findout My Apps > Apps\n"
            "5. if you already have API Token copy then, otherwise click Generate\n"
            "Note: API Token is always started with 'pk_'")

        update.message.reply_text("Reply on *this message* with your api key", parse_mode="Markdown",
                                  reply_markup=ForceReply())


def set_api_user_input(update: Updater, context: CallbackContext):
    """
    Hypothesis 1: blank user input
    Research: Unpossible, reply window closed

    Hypothesis 2: is possible to re-reply message:
    Research: Possible

    Hypothesis 3: other command will handle window closing?
    Research:

    """
    user_input = update.message.text
    if context.user_data["status"] == 0:
        if user_input.startswith('pk_'):
            request = infinity.check_authorisation(user_input)
            try:
                if request["user"]:

                    DB.new_user(context.user_data["user_id"], user_input)
                    user_workspaces = infinity.get_list_of_workspaces(user_input)
                    """
                    Hypothesis 1: So can user delete only one existing workspace
                    Research: Yes, but then he will have only one opportunity > to create a new one
                    """
                    """
                    check if user
                    """
                    if len(user_workspaces) > 0:
                        # insert global workspaces associated with user
                        for workspace_name, workspace_id in user_workspaces.items():
                            DB.insert_spaces(context.user_data["user_id"], workspace_name, workspace_id)

                            user_spaces = infinity.get_user_spaces(user_input, workspace_id)
                            # insert spaces inside global spaces
                            if len(user_spaces) > 0:

                                for space_name, space_id in user_spaces.items():
                                    DB.insert_user_spaces(context.user_data["user_id"], workspace_id, space_name,
                                                          space_id)

                                    user_lists = infinity.get_user_lists(user_input, space_id)
                                    # fill user lists
                                    if len(user_lists) > 0:
                                        for list_name, list_id in user_lists.items():
                                            DB.insert_user_lists(context.user_data["user_id"], space_id, list_name,
                                                                 list_id)

                                    else:
                                        DB.rollback_set_api(context.user_data["user_id"])
                                        raise CustomException.CustomException("User does not have any folderless lists")
                            else:
                                DB.rollback_set_api(context.user_data["user_id"])
                                raise CustomException("User have no active Spaces")

                        button = [[InlineKeyboardButton("Setup your workspace", callback_data="setup_workspace")]]
                        markup = InlineKeyboardMarkup(button)

                        context.user_data["status"] = 1
                        update.message.reply_text(f"Hey {request['user']['username']}, Welcome to SPLUST_BOT\n\n",
                                                  reply_markup=markup)

                    else:
                        DB.rollback_set_api(context.user_data["user_id"])
                        raise CustomException.CustomException("User is not associated with Workspaces")


            except KeyError:
                update.message.reply_text("Evil demons prevent us from accessing your boards :) Try one more time!")
                update.message.reply_text("Reply on *this message* with your api key", parse_mode="Markdown",
                                          reply_markup=ForceReply())
            except CustomException.CustomException as Error:
                update.message.reply_text(f"{Error}")

        else:
            update.message.reply_text("Looks like your api doesnt match, basically api looks like 'pk_...'")
            update.message.reply_text("Reply on *this message* with your api key", parse_mode="Markdown",
                                      reply_markup=ForceReply())


def keyboard_callbacks(update: Updater, context: CallbackContext):
    query = update.callback_query

    if query.data == "setup_workspace":
        workspaces = DB.get_workspace_list(context.user_data["user_id"])


        # dynamic keyboard
        IKB = [InlineKeyboardButton(f"{key}", callback_data=f"{value}") for key, value in workspaces.items()]
        button = [IKB[i:i + 2] for i in range(0, len(IKB), 2)]
        markup = InlineKeyboardMarkup(button)

        query.edit_message_text("Lets setup your Flow\n\n\nChoose Workspace you will work in:", reply_markup=markup)
        pass
    # if query.data in callbacks containg workspace_id's. Lets querry for spaces >

    if query.data in [str(i) for i in list(DB.get_workspace_list(context.user_data["user_id"]).values())]:
        userspaces = DB.get_space_list(context.user_data["user_id"], query.data)

        # dynamic keyboard
        IKB = [InlineKeyboardButton(f"{key}", callback_data=f"{value}") for key, value in userspaces.items()]
        button = [IKB[i:i + 2] for i in range(0, len(IKB), 2)]
        markup = InlineKeyboardMarkup(button)

        query.edit_message_text("Got it! Lets choose your Space:", reply_markup=markup)

    # lets choose user_lists
    if query.data in [str(i) for i in list(DB.get_space_list(context.user_data["user_id"]).values())]:
        userlists = DB.get_space_lists_list(context.user_data["user_id"], query.data)

        # dynamic keyboard
        IKB = [InlineKeyboardButton(f"{key}", callback_data=f"{value}") for key, value in userlists.items()]
        button = [IKB[i:i + 2] for i in range(0, len(IKB), 2)]
        markup = InlineKeyboardMarkup(button)

        query.edit_message_text("Finally choose list you will work in: ", reply_markup=markup)

    # finalizing setup

    if query.data in [str(i) for i in list(DB.get_space_lists_list(context.user_data["user_id"]).values())]:
        DB.update_active_list(context.user_data["user_id"], query.data)
        context.user_data["active_list"] = DB.get_active_userspace(context.user_data["user_id"])

        updater.dispatcher.add_handler(MessageHandler(Filters.text, message_handler), group=3)

        query.edit_message_text("Thanks! Now your workspace is setted up!\n How to work with bot /help \n\n*Enjoy!*",
                                parse_mode="Markdown")

    # catching task creating messages

    if query.data == "do_task":
        description = str(query.message.text)[query.message.text.find("Would you like to create task?") + 33:]
        infinity.create_task(context.user_data["user_api"], description, context["active_list"][1])

        query.edit_message_text("Task will be saved")

    if query.data == "stop_task":
        query.edit_message_text("task will be not saved")


def message_handler(update: Updater, context: CallbackContext):
    user_input = update.message.text

    keyboard = [
        [InlineKeyboardButton("Yes", callback_data="do_task"),
         InlineKeyboardButton("No", callback_data="stop_task")]
    ]
    markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text(f'Your workspace is *{context.user_data["active_list"][0]}* Would you like to create '
                              f'task?\n\n{user_input}', parse_mode="Markdown", reply_markup=markup)


def refresh(update: Updater, context: CallbackContext):
    DB.rollback_set_api(context.user_data["user_id"])
    context.user_data["status"] = 0


updater.dispatcher.add_handler(MessageHandler(Filters.all, backlog_checker), group=0)

updater.dispatcher.add_handler(CommandHandler("start", start), group=0)
updater.dispatcher.add_handler(CommandHandler("set_api", set_api), group=1)
updater.dispatcher.add_handler(CommandHandler("refresh", refresh), group=1)
updater.dispatcher.add_handler(MessageHandler(Filters.reply, set_api_user_input), group=1)

updater.dispatcher.add_handler(CallbackQueryHandler(keyboard_callbacks), group=2)

print("Started ...")
updater.start_polling()
updater.idle()
