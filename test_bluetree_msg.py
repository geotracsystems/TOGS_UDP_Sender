import sys
from string import Template
from utils.bep_helper import *
from utils.send_udp import send_udp


message_frame_start = 'AA 55 '              # Message Frame Start (constant)
message_frame_end = 'C9 17 '                # Message Frame End (constant)

bep_header_template = Template(
    '$imei 00 01 01 01 $seqno $length $eventid 00 00 50 11 '
)

bep_body_template = Template(
    '01 A0 $gp1 04 55 A9 F8 05 04 DC 3A 1D D1 '
)


seqno = 1

if len(sys.argv) != 9:
    print("Invalid arguments")
    print(len(sys.argv))
    print("Usage 1:\n", sys.argv[0], "<imei> <host> <port> <filename>")
    print("Usage 2:\n", sys.argv[0], "<esn> <host> <port> single <latitude> <longitude> <speed> <eventid>")
    exit()

esn = int(sys.argv[1])
host = sys.argv[2]
port = int(sys.argv[3])


if sys.argv[4] == 'single':
    latitude = sys.argv[5]
    longitude = sys.argv[6]
    speed = int(sys.argv[7])
    eventid = int(sys.argv[8])


bep_body = bep_body_template.substitute(gp1=nmea_sentence(latitude, longitude, speed))
full_length_hex = hex(int(len(bep_body)/3 + 24)).replace('x', '').upper().zfill(4)
length_format = f'{full_length_hex[2:4]} {full_length_hex[0:2]}'

bep_header = bep_header_template.substitute(imei=bep_esn(esn), length=length_format, seqno=bep_seq(seqno),
                                            eventid=bep_event(eventid))


bep_message = message_frame_start + bep_header + bep_body + message_frame_end
print(bep_message)
print(len(bep_message)/3)

response = send_udp(host, port, bep_message)
