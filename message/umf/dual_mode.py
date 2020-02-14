
"""

   message.umf.dual_mode.AVL ()

"""
from message.umf import umf_wrap_body, umf_named_payload, umf_gps_time, message_template, sized_hex

def AVL(args):
    esn, seqno, eventid, lat, lon, rssi, speed, heading, odo = ( args.esn, args.seqno, args.event_id, args.latitude, args.longitude, args.rssi, args.speed, args.heading, args.odo)
    body = message_template.umf_dual_AVL.substitute(
            eventid = sized_hex(eventid,1),
            gps_timestamp = umf_gps_time(lat, lon),
            rssi = sized_hex(rssi,1),
            speed = sized_hex(speed,2),
            heading = sized_hex(heading,2),
            odo = sized_hex(odo,4)
        )
    if ('-named' in args.custom_args):
        body = umf_named_payload(body,'Dual-ModeAVL')

    return umf_wrap_body(
        body, esn, seqno
    )