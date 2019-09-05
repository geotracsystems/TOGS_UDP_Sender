from utils.lmdirect_helper import *
from utils.send_udp import send_udp
from time import sleep
import random
import sys


lmdirect_message = "83 05 00 00 00 00 00 01 01 01 02 00 00 00 00 00 00 00 00 00 00 12 FB F5 B0 C3 04 17 01 00 01 49 A8 00 00 00 00 00 0E 08 00 00 00 00 00 0F 0A 01 00 15 00 01 00 01 97 21 C9"


def main():
    seqno = 1

    if len(sys.argv) != 5:
        print("This test requires exactly 4 arguments.")
        print("Usage:", sys.argv[0], "<esn> <host> <port> <filename>")
        sys.exit()

    esn = int(sys.argv[1])
    host = sys.argv[2]
    port = int(sys.argv[3])
    filename = sys.argv[4]

    f = open(filename)
    line = f.readline()

    while line:
        timestamp = unixtime_to_hexstring()
        msgtype = line.rstrip()

        populated_line = (lmdirect_message[0:6] + lmdirect_esn_converter(esn) + lmdirect_message[20:33] +
                          hex_sequence_number(seqno) + " " + timestamp + " " + timestamp + " " +
                          lmdirect_message[63:149] + " " + msgtype + lmdirect_message[152:]).upper()
        print(populated_line)
        print("Sending line", seqno, "from", filename)
        response = send_udp(host, port, populated_line)

        print("Received Ack for line", seqno, ":", response)

        sleep(random.randint(1, 5))

        line = f.readline()
        seqno += 1

    f.close()


main()
