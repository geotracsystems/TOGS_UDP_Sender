import csv
import argparse
from time import sleep
from string import Template
from utils.bep_helper import *
from utils.send_udp import send_udp
from utils.logger import logger

log = logger(__file__)

message_frame_start = 'AA 55 '              # Message Frame Start (constant)
message_frame_end = 'C9 17 '                # Message Frame End (constant)

bep_header_template = Template(
    '$imei 00 01 01 01 $seqno $length $eventid 00 00 50 11 '
)

bep_body_template = Template(
    '01 A0 $gp1 04 55 A9 F8 05 04 DC 3A 1D D1 '
)


def make_bep_message(esn, seqno, eventid, latitude, longitude, speed):
    bep_body = bep_body_template.substitute(gp1=nmea_sentence(latitude, longitude, speed))
    full_length_hex = hex(int(len(bep_body) / 3 + 24)).replace('x', '').upper().zfill(4)
    length_format = f'{full_length_hex[2:4]} {full_length_hex[0:2]}'

    bep_header = bep_header_template.substitute(imei=bep_esn(esn), length=length_format, seqno=bep_seq(seqno),
                                                eventid=bep_event(eventid))

    bep_message = message_frame_start + bep_header + bep_body + message_frame_end
    return bep_message


seqno = 1

parser = argparse.ArgumentParser(description="Send Bluetree BEP Messages")
parser.add_argument("host", help="Hostname or IP address of Backend", type=str)
parser.add_argument("port", help="Backend port", type=int)
parser.add_argument("modem", help="The word bluetree", type=str, choices=["bluetree"])

subparsers = parser.add_subparsers(description="Send Modes", dest="send_mode")

single_parser = subparsers.add_parser("single", help="Sends a single UDP message")
single_parser.add_argument("esn", help="ESN", type=int)
single_parser.add_argument("latitude", help="Latitude in decimal", type=str)
single_parser.add_argument("longitude", help="Longitude in decimal", type=str)
single_parser.add_argument("speed", help="Speed in km/h", type=int)
single_parser.add_argument("event_id", help="Event ID", type=int)

csv_parser = subparsers.add_parser("csv", help="Sends multiple UDP messages based on CSV file")
csv_parser.add_argument("file", help="Filename")

args = parser.parse_args()

host = args.host
port = args.port

if args.send_mode == 'single':
    log.debug("Single Message mode")
    esn = args.esn
    latitude = args.latitude
    longitude = args.longitude
    speed = args.speed
    eventid = args.event_id
    bep_message = make_bep_message(esn, seqno, eventid, latitude, longitude, speed)
    log.info("Sending single line")
    log.info(bep_message)
    response = send_udp(host, port, bep_message)
    log.info("Received Ack")
    log.info(response)
elif args.send_mode == 'csv':
    log.debug("CSV mode")
    filename = args.file
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
                bep_message = make_bep_message(esn, seqno, eventid, latitude, longitude, speed)
                log.info(f"Sending line {lc} from {filename}\n{bep_message}")
                response = send_udp(host, port, bep_message)
                log.info("Received Ack")
                log.info(response)
                lc = lc + 1
            seqno = seqno + 1
            sleep(2)
