import socket
from time import sleep
from time import time


def send_udp(host, port, data):
    """Simply send UDP Data to a given Host and Port and print out the response if any"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    sock.sendto(bytes.fromhex(data), (host, port))

    d = sock.recvfrom(1024)
    ack = d[0]

    sock.close()
    return str(ack)


def is_calamp_esn_valid(esn):
    """Validate Calamp ESN"""
    if isinstance(esn, int) and (len(str(esn)) == 10):
        return True
    else:
        return False


def lmdirect_esn_converter(esn):
    """Convert a valid Calamp ESN to Calamp's "Human Readable" Hex Format"""
    if not is_calamp_esn_valid(esn):
        print("Invalid ESN. Terminating Test.")
        raise SystemExit

    esnsting = str(esn)
    lmdirect_esn = esnsting[0] + esnsting[1] + " " + esnsting[2] + esnsting[3] + " " + esnsting[4] + esnsting[5] + " " + esnsting[6] + esnsting[7] + " " + esnsting[8] + esnsting[9]
    return lmdirect_esn


def unixtime_to_hexstring():
    """Convert current unix time to a Hex String in Little Endian"""
    ts = time()
    timestamp = str(hex(int(ts)))
    hextimestamp = timestamp[2] + timestamp[3] + " " + timestamp[4] + timestamp[5] + " " + timestamp[6] + timestamp[7] + " " + timestamp[8] + timestamp[9]
    return hextimestamp

def hex_sequence_number(seqno):
    """Convert an int seqno to 2-byte hex in Little Endian"""
    hexseq = format(seqno, '04x')
    seq = hexseq[0] + hexseq[1] + " " + hexseq[2] + hexseq[3]
    return seq


