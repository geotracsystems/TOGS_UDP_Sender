import sys
import csv
from time import sleep
from string import Template
from utils.lmdirect_helper import *
from utils.send_udp import send_udp


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

if len(sys.argv) != 9 and len(sys.argv) != 5:
    print("Invalid arguments")
    print(len(sys.argv))
    print("Usage 1:\n", sys.argv[0], "<esn> <host> <port> <filename>")
    print("Usage 2:\n", sys.argv[0], "<esn> <host> <port> single <latitude> <longitude> <speed> <eventid>")
    sys.exit()

esn = int(sys.argv[1])
host = sys.argv[2]
port = int(sys.argv[3])

if sys.argv[4] == 'single':
    latitude = sys.argv[5]
    longitude = sys.argv[6]
    speed = int(sys.argv[7])
    eventid = int(sys.argv[8])
    lmdirect_message = make_lmdirect_message(esn, seqno, eventid, latitude, longitude, speed)
    print("Sending single line\n", lmdirect_message)
    response = send_udp(host, port, lmdirect_message)
    print("Received Ack\n", response)
elif sys.argv[4] != 'single' and len(sys.argv) == 5:
    filename = sys.argv[4]
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
                latitude = row[0]
                longitude = row[1]
                speed = int(row[2])
                eventid = int(row[3])
                lmdirect_message = make_lmdirect_message(esn, seqno, eventid, latitude, longitude, speed)
                print(f"Sending line {lc} from {filename}\n{lmdirect_message}")
                response = send_udp(host, port, lmdirect_message)
                print("Received Ack\n", response)
                lc = lc + 1
            seqno = seqno + 1
            sleep(3)
