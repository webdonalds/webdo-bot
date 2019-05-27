from datetime import datetime, timezone, timedelta
import threading

from libs import delivery
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

!택배 <택배사> <운송장번호>
Example: !택배 CJ대한통운 1234567890
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


def cmd_delivery(subcommands, bot, update):
    """
    !택배 <택배사> <운송장번호>
    """
    
    carrier_name = subcommands[0]
    track_id = subcommands[1]

    carriers = list(filter(lambda c: carrier_name in c['name'], delivery.list_carriers()))
    if len(carriers) == 0:
        _reply_text(f"해당하는 이름의 택배사가 없습니다 : {carrier_name}", bot, update)
        return
    elif len(carriers) > 1:
        msg = '해당하는 이름의 택배사가 여러 개 있습니다.'
        for c in carriers:
            msg += f"\n - {c['name']}"
        _reply_text(msg, bot, update)
        return

    _track_delivery(carriers[0], track_id, bot, update, first_call=True)


def _track_delivery(carrier, track_id, bot, update, first_call=False):
    track = delivery.get_tracking(carrier['id'], track_id)
    msg = f"\n[배송 정보]\n운송장 번호 : {track_id}\n"

    follow_up = False
    if 'progresses' in track and len(track['progresses']) == 0:
        if first_call:
            msg += '배송 준비중입니다.'
            _reply_text(msg, bot, update)

        follow_up = True
    elif 'progresses' in track and len(track['progresses']) > 0:
        current = sorted(track['progresses'], key=lambda p: p['time'])[-1]
        if current['status']['id'] == 'delivered':
            msg += '배송이 완료되었습니다.'
            _reply_text(msg, bot, update)
        else:
            dt = datetime.strptime(current['time'], '%Y-%m-%dT%H:%M:%S%z')
            if first_call or dt >= (datetime.now(timezone.utc) - timedelta(minutes=30)):
                msg += f"상태 : {current['status']['text']}\n" + \
                    f"위치 : {current['location']['name']}\n\n" + \
                    f"{current['description']}\n" + \
                    f"(업데이트 : {(datetime.now(timezone.utc) - dt).seconds // 60}분 전)"
                _reply_text(msg, bot, update)
            
            follow_up = True
    else:
        msg += "올바르지 않은 운송장이거나, 택배사에서 아직 물건을 인수하지 않았습니다."
        _reply_text(msg, bot, update)

    if follow_up:
        def schedule():
            import sched
            import time

            scheduler = sched.scheduler(time.time, time.sleep)
            scheduler.enter(30 * 60, 1, _track_delivery, argument=(carrier, track_id, bot, update))
            scheduler.run()
        
        thread = threading.Thread(target=schedule)
        thread.start()

        if first_call:
            _reply_text('배송 내역에 변경이 있을 시 30분 간격으로 알림이 발송됩니다.', bot, update)
