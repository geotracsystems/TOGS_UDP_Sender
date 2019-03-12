import socket


def send_udp(host, port, data):
    """Simply send UDP Data to a given Host and Port and print out the response if any"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(5)

    sock.sendto(bytes.fromhex(data), (host, port))

    try:
        d = sock.recvfrom(1024)
    except socket.timeout:
        print("ERROR: Message timed out")
        return

    ack = d[0]
    sock.close()
    return str(ack)
