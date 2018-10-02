import togs_helper as th
from time import sleep
import random
import sys


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
        timestamp = th.unixtime_to_hexstring()
        splitline = line.split('#', 1)
        hexmsg = splitline[0].rstrip()

        populated_line = (hexmsg[0:6] + th.lmdirect_esn_converter(esn) + hexmsg[20:33] + th.hex_sequence_number(seqno) + " " + timestamp + " " + timestamp + " " + hexmsg[63:]).upper()
        print(populated_line)
        print("Sending line", seqno, "from", filename)
        response = th.send_udp(host, port, populated_line)

        print("Received Ack for line", seqno, ":", response)

        sleep(random.randint(1, 5))

        line = f.readline()
        seqno += 1

    f.close()


main()


# Accept cL arguments Host, Port, File
# Make data file
