from utils.lmdirect_helper import *
from utils.send_udp import send_udp
from time import sleep
import sys


lmdirect_message = "83 05 00 00 00 00 00 01 01 01 02 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 0E 08 00 00 00 00 00 0F 0A 01 00 15 0A 01 00 01 97 21 C9"


def main():
    seqno = 1
    port = 6080

    if len(sys.argv) != 4:
        print("This test requires exactly 4 arguments.")
        print("Usage:", sys.argv[0], "<esn> <host> <filename>")
        sys.exit()

    esn = int(sys.argv[1])
    host = sys.argv[2]
    filename = sys.argv[3]

    f = open(filename)
    line = f.readline()

    while line:
        timestamp = unixtime_to_hexstring()
        gpsdata = line.split(",")
        latitude = gpsdata[0].strip()
        longitude = gpsdata[1].strip()
        speed = int(gpsdata[2].strip())

        coordinates = lmdirect_gps(latitude, longitude)
        hex_speed = lmdirect_speed(speed)

        # print(coordinates)
        # print(hex_speed)

        populated_line = (lmdirect_message[0:6] + lmdirect_esn_converter(esn) + lmdirect_message[20:33] +
                          hex_sequence_number(seqno) + " " + timestamp + " " + timestamp + " " + coordinates + " " +
                          hex_speed + " " + lmdirect_message[111:]).upper()

        print(populated_line)
        print("Sending coordinates from line", seqno, "from", filename)
        response = send_udp(host, port, populated_line)
        print("Received Ack for line", seqno, ":", response, "\n")

        line = f.readline()
        seqno += 1
        sleep(1)


main()
