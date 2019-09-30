import csv
import argparse
from time import sleep
from string import Template
from utils.lmdirect_helper import *
from utils.send_udp import send_udp
from utils.logger import logger


log = logger(__file__)

lmdirect_message_template = Template(
    '83 05 $esn 01 01 01 02 $seqno $timestamp1 $timestamp2 $coordinates $speed 00 0E 08 00 00 00 00 00 0F 0A 01 00 FF $eventid 01 00 01 97 21 C9'
)


def make_lmdirect_message(esn, seqno, eventid, latitude, longitude, speed):
    lmdirect_message = lmdirect_message_template.substitute(esn=lmdirect_esn_converter(esn),
                                                            seqno=hex_sequence_number(seqno),
                                                            timestamp1=unixtime_to_hexstring(),
                                                            timestamp2=unixtime_to_hexstring(),
                                                            coordinates=lmdirect_gps(latitude, longitude),
                                                            speed=lmdirect_speed(speed),
                                                            eventid=lmdirect_event(eventid))
    return lmdirect_message


seqno = 1

parser = argparse.ArgumentParser(description="Send Bluetree BEP Messages")
parser.add_argument("host", help="Hostname or IP address of Backend", type=str)
parser.add_argument("port", help="Backend port", type=int)
parser.add_argument("modem", help="The word calamp", type=str, choices=["calamp"])

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
    lmdirect_message = make_lmdirect_message(esn, seqno, eventid, latitude, longitude, speed)
    log.info("Sending single line")
    log.info(lmdirect_message)
    response = send_udp(host, port, lmdirect_message)
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
                lmdirect_message = make_lmdirect_message(esn, seqno, eventid, latitude, longitude, speed)
                log.info(f"Sending line {lc} from {filename}\n{lmdirect_message}")
                response = send_udp(host, port, lmdirect_message)
                log.info("Received Ack")
                log.info(response)
                lc = lc + 1
            seqno = seqno + 1
            sleep(2)
