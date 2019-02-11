import threading

from parsers import *


def _reply_text(text, bot, update):
    reply_text = f"@{update.message.from_user.username} {text}"
    bot.send_message(update.message.chat.id, reply_text)


def cmd_help(subcommands, bot, update):
    """
    Reply all commands.
    """

    help_text = """
!ping

!timer <time> <text>
!타이머 <time> <text>
Example: !timer 3m 라면 불 끄기

... and some hidden commands!
    """
    _reply_text(help_text, bot, update)


def cmd_ping(subcommands, bot, update):
    """
    !ping
    """
    _reply_text('pong', bot, update)


def cmd_timer(subcommands, bot, update):
    """
    !timer <time> <text>
      - time (time string) : waiting time
      - text (string)      : text of message for timer alert
    """
    try:
        seconds = parse_time_str(subcommands[0])
    except ParseError:
        _reply_text(f"Invalid format: {subcommands[0]}", bot, update)
        return

    if seconds > 60 * 60 * 24:
        _reply_text('Time too long', bot, update)
        return

    def schedule():
        import sched
        import time

        text = ' '.join(subcommands[1:])

        scheduler = sched.scheduler(time.time, time.sleep)
        scheduler.enter(seconds, 1, _reply_text, argument=(text, bot, update))
        scheduler.run()

    thread = threading.Thread(target=schedule)
    thread.start()

    _reply_text('Timer has been started.', bot, update)
