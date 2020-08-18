import csv
from time import sleep, time
from string import Template
from utils.bep_helper import *
from utils.lmdirect_helper import *
from utils.send_udp import send_udp
from utils.logger import logger
from gooey import Gooey, GooeyParser


log = logger(__file__)

message_frame_start = 'AA 55 '              # Message Frame Start (constant)
message_frame_end = 'C9 17 '                # Message Frame End (constant)

bep_header_template = Template(
    '$imei 00 01 01 01 $seqno $length $eventid 00 00 50 11 '
)

bep_body_template = Template(
    '01 A0 $gp1 04 55 A9 F8 05 04 DC 3A 1D D1 '
)

lmdirect_message_template = Template(
    '83 05 $esn 01 01 01 02 $seqno $timestamp1 $timestamp2 $coordinates $speed 00 0E 08 00 00 00 00 00 0F 0A 01 00 FF $eventid 01 00 01 97 21 C9'
)


def make_lmdirect_message(esn, seqno, eventid, latitude, longitude, speed, msgtime):
    lmdirect_message = lmdirect_message_template.substitute(esn=lmdirect_esn_converter(esn),
                                                            seqno=hex_sequence_number(seqno),
                                                            timestamp1=unixtime_to_hexstring(msgtime),
                                                            timestamp2=unixtime_to_hexstring(msgtime),
                                                            coordinates=lmdirect_gps(latitude, longitude),
                                                            speed=lmdirect_speed(speed),
                                                            eventid=lmdirect_event(eventid))
    return lmdirect_message


def make_bep_message(esn, seqno, eventid, latitude, longitude, speed, msgtime):
    bep_body = bep_body_template.substitute(gp1=nmea_sentence(latitude, longitude, speed, msgtime))
    full_length_hex = hex(int(len(bep_body) / 3 + 24)).replace('x', '').upper().zfill(4)
    length_format = f'{full_length_hex[2:4]} {full_length_hex[0:2]}'

    bep_header = bep_header_template.substitute(imei=bep_esn(esn), length=length_format, seqno=bep_seq(seqno),
                                                eventid=bep_event(eventid))

    bep_message = message_frame_start + bep_header + bep_body + message_frame_end
    return bep_message


@Gooey(default_size=(600, 750),
       program_name=f'TOGS UDP Sender',
       show_restart_button=False,
       navigation='TABBED',
       show_success_modal=False,
       terminal_font_family='TELETYPE',
       terminal_font_color='#000000',
       )
def main():
    seqno = 1

    parser = GooeyParser(description="Send Bluetree and Calamp UDP Messages")

    subparsers = parser.add_subparsers(dest="send_mode")

    single_parser = subparsers.add_parser("single", help="Sends a single UDP message")
    single_parser.add_argument("modem", help="Modem Type", type=str, choices=["bluetree", "calamp"])
    single_parser.add_argument("host", help="Hostname or IP address of Backend", type=str)
    single_parser.add_argument("port", help="Backend port", type=int)
    single_parser.add_argument("esn", help="ESN", type=int)
    single_parser.add_argument("latitude", help="Latitude in decimal", type=str)
    single_parser.add_argument("longitude", help="Longitude in decimal", type=str)
    single_parser.add_argument("speed", help="Speed in km/h", type=int)
    single_parser.add_argument("event_id", help="Event ID", type=int)
    single_parser.add_argument("--MessageTime",
                               help="Origination Time of Message (unixtime) (if blank, current time is sent)",
                               type=int, required=False)

    csv_parser = subparsers.add_parser("csv", help="Sends multiple UDP messages based on CSV file")
    csv_parser.add_argument("modem", help="Modem Type", type=str, choices=["bluetree", "calamp"])
    csv_parser.add_argument("host", help="Hostname or IP address of Backend", type=str)
    csv_parser.add_argument("port", help="Backend port", type=int)
    csv_parser.add_argument("file", help="Filename", widget='FileChooser')
    csv_parser.add_argument("delay", help="Time between messages (s)", type=int)

    args = parser.parse_args()

    if args.send_mode == 'single':
        log.debug("Single Message mode")
        host = args.host
        port = args.port
        esn = args.esn
        modem = args.modem
        latitude = args.latitude
        longitude = args.longitude
        speed = args.speed
        eventid = args.event_id

        if args.MessageTime is None:
            msgtime = time()
        else:
            msgtime = args.MessageTime

        if modem == 'bluetree':
            message = make_bep_message(esn, seqno, eventid, latitude, longitude, speed, msgtime)
        elif modem == 'calamp':
            message = make_lmdirect_message(esn, seqno, eventid, latitude, longitude, speed, msgtime)
        log.info("Sending single line")
        log.info(message)
        response = send_udp(host, port, message)
        log.info("Received Ack")
        log.info(response)
    elif args.send_mode == 'csv':
        log.debug("CSV mode")
        host = args.host
        port = args.port
        modem = args.modem
        filename = args.file
        delay = args.delay
        column_names = []
        with open(filename) as csv_file:
            lc = 0
            csv_reader = csv.reader(csv_file)
            for row in csv_reader:
                if lc == 0:
                    for item in row:
                        column_names.append(item)
                    lc = lc + 1
                else:
                    esn = int(row[0])
                    latitude = row[1]
                    longitude = row[2]
                    speed = int(row[3])
                    eventid = int(row[4])

                    try:
                        msgtime = int(row[5])
                    except IndexError:
                        msgtime = time()

                    if modem == 'bluetree':
                        message = make_bep_message(esn, seqno, eventid, latitude, longitude, speed, msgtime)
                    elif modem == 'calamp':
                        message = make_lmdirect_message(esn, seqno, eventid, latitude, longitude, speed, msgtime)
                    log.info(f"Sending line {lc} from {filename}\n{message}")
                    response = send_udp(host, port, message)
                    log.info("Received Ack")
                    log.info(response)
                    lc = lc + 1
                seqno = seqno + 1
                sleep(delay)


if __name__ == "__main__":
    main()
