"""

   create UMF OOTN messages

"""

from enum import Enum 
from message.umf import umf_wrap_body, umf_named_payload, sized_hex, message_template, umf_gps_time, umf_time

class OOTN(Enum):#num # args
    BEGIN_TIMER     = '00' # gps(10) + timer(2)
    BACK_IN_VEHICLE = '01' # gps(10)
    SOUND_ALARM     = '02' # utc(4)
    TIMER_CONFIRM   = '03' # timer(2)
    STOP_TIMER      = '04' # utc(4)


def begin_timer(args):
    esn, seqno, lat, lon, mins = (args.esn, args.seqno, args.latitude, args.longitude, args.timer)
    body = message_template.umf_ootn.substitute(
            type = OOTN.BEGIN_TIMER.value,
            args = umf_gps_time(lat, lon) + ' ' + sized_hex(mins, 2)
        )

    if ('-named' in args.custom_args):
        body = umf_named_payload(body,'OOTN.BeginTimer')

    return umf_wrap_body(
        body, esn, seqno
    )


def back_in_vehicle(args):
    esn, seqno, lat, lon = ( args.esn, args.seqno, args.latitude, args.longitude)
    body = message_template.umf_ootn.substitute(
            type = OOTN.BACK_IN_VEHICLE.value,
            args = umf_gps_time(lat, lon)
        )

    if ('-named' in args.custom_args):
        body = umf_named_payload(body,'OOTN.TimerConfirmation')

    return umf_wrap_body(
        body, esn, seqno
    )


def sound_alarm(args):
    esn, seqno = (args.esn, args.seqno)
    body = message_template.umf_ootn.substitute(
            type = OOTN.SOUND_ALARM.value,
            args = umf_time()
        )

    if ('-named' in args.custom_args):
        body = umf_named_payload(body,'OOTN.SoundAlarm')

    return umf_wrap_body(
        body, esn, seqno
    )


def confirm_timer(args):
    esn, seqno, mins = ( args.esn, args.seqno, args.timer)
    body = message_template.umf_ootn.substitute(
            type = OOTN.TIMER_CONFIRM.value,
            args = sized_hex(mins, 2)
        )

    if ('-named' in args.custom_args):
        body = umf_named_payload(body,'OOTN.TimerConfirmation')

    return umf_wrap_body(
        body, esn, seqno
    )


def stop_timer(args):
    esn, seqno = ( args.esn, args.seqno)
    body = message_template.umf_ootn.substitute(
            type = OOTN.STOP_TIMER.value,
            args = umf_time()
        )

    if ('-named' in args.custom_args):
        body = umf_named_payload(body,'OOTN.StopTimer')

    return umf_wrap_body(
        body, esn, seqno
    )

