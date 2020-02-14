import message.templates as message_template
from utils.umf_helper import sized_hex, umf_crc16, umf_gps_time, umf_time


def umf_wrap_body(body, esn, seqno):
    bodyLen = len(bytes.fromhex(body))
    header = message_template.umf_header.substitute(
        esn = sized_hex( esn, 8),
        seq = sized_hex( seqno, 2),
        len = sized_hex( bodyLen, 2)
        )
    #print(header + ' ' +  body)
    return message_template.umf.substitute(
        header = header,
        body = body,
        chksum = sized_hex( umf_crc16(header+' '+body), 2)
    )


def umf_named_payload(payload, name):
    bodyLen = len(bytes.fromhex(payload))
    return message_template.umf_named_payload.substitute(
        name = sized_hex(name, len(name) + 1), #TODO: test that this null terminates
        body = payload,
        len = sized_hex( bodyLen, 2)
    )


from . import dual_mode
from . import ootn
