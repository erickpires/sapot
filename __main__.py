#!/usr/bin/env python3

from sapot import get_process_status, process_step_to_string, process_to_string
from utils import *
import os
import sys
import logging

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from dotenv import load_dotenv

# Loading the .env configuration file
load_dotenv()

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

# TODO(erick): Avoid the current_handled_chats map from getting to big.
current_handled_chats = {}

def get_chat_id(update):
    return update.message.chat.id

# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Use the /status command to know the current status of a process.\n'+
                              'Use the /describe command to view all the history of a process.')

def status(update, context):
    """Send a message when the command /status is issued."""

    current_handled_chats[get_chat_id(update)] = 'status'
    update.message.reply_text('What\'s the ID of the process you\'re interested in?')

def describe(update, context):
    """Send a message when the command /status is issued."""

    current_handled_chats[get_chat_id(update)] = 'describe'
    update.message.reply_text('What\'s the ID of the process you\'re interested in?')


def echo(update, context):
    """Handle user messages."""

    chat_id = get_chat_id(update)

    if not chat_id in current_handled_chats:
        update.message.reply_text('Please, use one of the available commands')
        return

    try:
        process_id = update.message.text
        process_status = get_process_status(process_id)

        action = current_handled_chats[chat_id]

        if action == 'status':
            response = process_step_to_string(process_status[0])
        else:
            response = process_to_string(process_status)

        update.message.reply_text(response)
    except:
        update.message.reply_text('An error occurred while trying to get process data.')

    del(current_handled_chats[chat_id])

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    """Start the bot."""

    updater = Updater(os.environ['TELEGRAM_TOKEN'], use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands
    dp.add_handler(CommandHandler('status', status))
    dp.add_handler(CommandHandler('describe', describe))
    dp.add_handler(CommandHandler('help', help))

    # on noncommand i.e message
    dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
