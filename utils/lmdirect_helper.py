from time import time
from decimal import Decimal


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
    lmdirect_esn = f'{esnsting[0:2]} {esnsting[2:4]} {esnsting[4:6]} {esnsting[6:8]} {esnsting[8:10]}'
    return lmdirect_esn


def unixtime_to_hexstring():
    """Convert current unix time to a Hex String in Little Endian"""
    ts = time()
    timestamp = str(hex(int(ts))).replace('0x', '').upper()
    hextimestamp = f'{timestamp[0:2]} {timestamp[2:4]} {timestamp[4:6]} {timestamp[6:8]}'
    return hextimestamp


def hex_sequence_number(seqno):
    """Convert an int seqno to 2-byte hex in Little Endian"""
    hexseq = format(seqno, '04X')
    seq = hexseq[0:2] + " " + hexseq[2:4]
    return seq


def lmdirect_event(eventid):
    """Convert decimal event ID to 1-byte hexadecimal event ID"""
    hexevent = format(eventid, '02X')
    return hexevent


def lmdirect_gps(latitude, longitude, altitude=0):
    """Convert floating point decimal latitude to Calamp coordinate string"""
    # Convert input coordinates from string to integer with 7 LSB's
    int_latitude = int(Decimal(latitude).quantize(Decimal('0.0000001')) * 10000000)
    int_longitude = int(Decimal(longitude).quantize(Decimal('0.0000001')) * 10000000)

    # Convert coordinates to Hex string
    hex_lat = str(hex((int_latitude + (1 << 32)) % (1 << 32))).replace('0x', '').upper().zfill(8)
    print(hex_lat)
    hex_long = str(hex((int_longitude + (1 << 32)) % (1 << 32))).replace('0x', '').upper().zfill(8)
    print(hex_long)
    hex_alt = '00 00 00 00'
    # Convert to coordinate string for LMDirect
    coordinates = (
        f'{hex_lat[0:2]} {hex_lat[2:4]} {hex_lat[4:6]} {hex_lat[6:8]} '
        f'{hex_long[0:2]} {hex_long[2:4]} {hex_long[4:6]} {hex_long[6:8]} '
        f'{hex_alt}'
    )
    # print(coordinates)
    return coordinates


def lmdirect_speed(speed):
    """Convert integer decimal speed in km/h to Calamp speed hex string (cm/s in Hex Little Endian) """
    speedcms = int(round(speed * 27.777778, 0))
    hexspeedcms = format(speedcms, '08x').upper()

    hex_speed = f'{hexspeedcms[0:2]} {hexspeedcms[2:4]} {hexspeedcms[4:6]} {hexspeedcms[6:8]}'
    return hex_speed
