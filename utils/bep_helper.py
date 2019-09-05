import time
from math import floor
from decimal import Decimal


def is_bt_imei_valid(imei):
    if isinstance(imei, int) and (len(str(imei)) == 15) and 350000000000000 <= imei <= 359999999999999:
        return True
    else:
        return False


def bep_esn(imei):
    if not is_bt_imei_valid(imei):
        print("Invalid Bluetree IMEI. Terminating test.")
        raise SystemExit
    heximei = str(hex(imei)).replace('x', '').upper()
    hex_bt_imei = (
        f'{heximei[12:14]} {heximei[10:12]} {heximei[8:10]} {heximei[6:8]} '
        f'{heximei[4:6]} {heximei[2:4]} {heximei[0:2]} 00'
    )
    return hex_bt_imei


def bep_seq(seqno):
    hexseq = str(hex(seqno)).replace('x', '').upper().zfill(8)
    seq = f'{hexseq[6:8]} {hexseq[4:6]} {hexseq[2:4]} {hexseq[0:2]}'
    return seq


def bep_event(eventid):
    hexevent = str(hex(eventid)).replace('x', '').upper().zfill(4)
    event = f'{hexevent[2:4]} {hexevent[0:2]}'
    return event


def nmea_sentence(latitude, longitude, speed):
    latitude_decimal = Decimal(latitude).quantize(Decimal('0.0000001'))
    longitude_decimal = Decimal(longitude).quantize(Decimal('0.0000001'))

    sentence_prefix = 'GPRMC'
    nmea_time = str(time.strftime('%H%M%S', time.gmtime()))
    rmc_status = 'A'

    lat_abs = abs(latitude_decimal)
    lat_deg = floor(lat_abs)
    lat_min = (lat_abs - lat_deg) * 60
    lat_pole = 'N' if latitude_decimal >= 0 else 'S'
    nmea_lat = f'{lat_deg:02}{lat_min:06.3f},{lat_pole}'

    lng_abs = abs(longitude_decimal)
    lng_deg = floor(lng_abs)
    lng_min = (lng_abs - lng_deg) * 60
    lng_pole = 'E' if longitude_decimal >= 0 else 'W'
    nmea_lng = f'{lng_deg:03}{lng_min:06.3f},{lng_pole}'

    knot_speed = f'{(speed*0.540):05.1f}'
    nmea_heading = '000.0'

    nmea_date = str(time.strftime('%d%m%y', time.gmtime()))
    nmea_magvar = '003.1,W'

    nmea_rmc_sentence = (
        f'{sentence_prefix},{nmea_time},{rmc_status},{nmea_lat},{nmea_lng},{knot_speed},{nmea_heading},'
        f'{nmea_date},{nmea_magvar}'
    )
    # print(nmea_rmc_sentence)
    checksum = 0
    for c in nmea_rmc_sentence:
        checksum = checksum ^ ord(c)
    checksum = checksum & 0xFF

    final_str = f'${nmea_rmc_sentence}*{checksum:02X}'
    len_str = len(final_str) + 2
    # print(final_str)
    # print(len_str)
    hex_str = ''
    for ch in final_str:
        hv = hex(ord(ch)).replace('0x', '').upper()
        hex_str = hex_str + hv + ' '
    hex_str = hex_str + '0D 0A'
    # print(hex_str)
    hex_length = f'{len_str:04X}'
    final_hex_str = f'{hex_length[2:4]} {hex_length[0:2]} {hex_str}'
    # print(final_hex_str)
    return final_hex_str

