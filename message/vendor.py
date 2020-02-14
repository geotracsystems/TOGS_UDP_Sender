
import message.templates as message_template

from utils.lmdirect_helper import lmdirect_esn_converter, lmdirect_gps, lmdirect_event, lmdirect_speed
from utils.lmdirect_helper import unixtime_to_hexstring, hex_sequence_number
from utils.bep_helper import bep_esn, bep_event, bep_seq, nmea_sentence


def lmdirect(args):
    (esn, seqno, eventid, latitude, longitude, speed) = ( args.esn, args.seqno, args.event_id, args.latitude, args.longitude, args.speed)
    lmdirect_message = message_template.lmdirect.substitute(esn=lmdirect_esn_converter(esn),
                                                            seqno=hex_sequence_number(seqno),
                                                            timestamp1=unixtime_to_hexstring(),
                                                            timestamp2=unixtime_to_hexstring(),
                                                            coordinates=lmdirect_gps(latitude, longitude),
                                                            speed=lmdirect_speed(speed),
                                                            eventid=lmdirect_event(eventid))
    return lmdirect_message


def bep(args):
    (esn, seqno, eventid, latitude, longitude, speed) = (args.esn, args.seqno, args.event_id, args.latitude, args.longitude, args.speed)
    bep_body = message_template.bep_body.substitute(gp1=nmea_sentence(latitude, longitude, speed))
    full_length_hex = hex(int(len(bep_body) / 3 + 24)).replace('x', '').upper().zfill(4)
    length_format = f'{full_length_hex[2:4]} {full_length_hex[0:2]}'

    bep_header = message_template.bep_header.substitute(
        imei=bep_esn(esn), length=length_format, seqno=bep_seq(seqno), eventid=bep_event(eventid))

    bep_message = message_template.frame_start + bep_header + bep_body + message_template.frame_end
    return bep_message
