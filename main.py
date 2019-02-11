import os
import logging

from telegram.ext import Updater, MessageHandler, Filters

from commands import *

logger = logging.getLogger(__name__)


def handle(bot, update):
    text = update.message.text
    if not text.startswith('!'):
        return
    
    cmds = text[1:].split(' ')
    if cmds[0] == 'ping':
        # !ping
        cmd_ping(cmds[1:], bot, update)
    elif cmds[0] in ['timer', '타이머']:
        # !timer <time> <message>
        cmd_timer(cmds[1:], bot, update)
    elif cmds[0] == '출근':
        # !출근
        cmd_timer(['9h', '퇴근시간입니다!'], bot, update)
    elif cmds[0] == 'help':
        # !help
        cmd_help([], bot, update)


def handle_error(bot, update, error):
    logger.warning(f"Update \"{update}\" caused error \"{error}\"")


if __name__ == '__main__':
    updater = Updater(os.environ['TELEGRAM_BOT_TOKEN'])

    dp = updater.dispatcher
    dp.add_handler(MessageHandler(Filters.text, handle))
    dp.add_error_handler(handle_error)

    updater.start_polling()
    updater.idle()
