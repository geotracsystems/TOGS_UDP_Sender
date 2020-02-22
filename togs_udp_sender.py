from collections import namedtuple
from gooey import Gooey, GooeyParser
from utils.send_udp import send_udp
from utils.logger import logger
from utils.umf_helper import umf_parse_response
from time import sleep
import csv

import message.vendor as vendor_message
import message.umf as umf_message

log = logger(__file__)

""" fancy names:
    -> add a new message type here so you can reference it with a linter to help
"""
bluetree =               'BlueTree'
calamp =                 'Calamp'
dual_avl =               'UMF_Dual_Mode_AVL'
ootn_sound_alarm =       'UMF_OOTN_Sound_Alarm'
ootn_back_in_vehicle =   'UMF_OOTN_Back_In_Vehicle'
ootn_begin_timer =       'UMF_OOTN_Begin_Timer'
ootn_timer_confirm =     'UMF_OOTN_Confirm_Timer'
ootn_stop_confirm =      'UMF_OOTN_Stop_Confirm'
admin_dual_eligability = 'Admin_Dual_Mode_Eligibility'
admin_network_change =   'Admin_Network_Medium_Change'

""" Message Constructors
    -> Add the message contructor here
"""
message_format_handlers = {
    bluetree:               vendor_message.bep,
    calamp:                 vendor_message.lmdirect,
    dual_avl:               umf_message.dual_mode.AVL,
    ootn_sound_alarm:       umf_message.ootn.sound_alarm,
    ootn_back_in_vehicle:   umf_message.ootn.back_in_vehicle,
    ootn_begin_timer:       umf_message.ootn.begin_timer,
    ootn_timer_confirm:     umf_message.ootn.confirm_timer,
    ootn_stop_confirm:      umf_message.ootn.stop_timer,
    admin_network_change:   umf_message.administration.network_medium_change,
    admin_dual_eligability: umf_message.administration.dual_mode_eligibility,
}

all_formats_fields = ['host', 'port', 'esn', 'seqno']

""" Format Required Fields
    -> add the agument the format needs here
"""
message_format_fields = {
    'CSV':                  ['file'],
    bluetree:               ['latitude', 'longitude', 'speed', 'event_id', 'seqno'],
    calamp:                 ['latitude', 'longitude', 'speed', 'event_id', 'seqno'],
    dual_avl:               ['latitude', 'longitude', 'speed', 'rssi', 'heading', 'odo', 'event_id', 'custom_args'],
    ootn_sound_alarm:       ['custom_args'],
    ootn_back_in_vehicle:   ['latitude', 'longitude', 'custom_args'],
    ootn_begin_timer:       ['latitude', 'longitude', 'timer', 'custom_args'],
    ootn_timer_confirm:     ['timer', 'custom_args'],
    ootn_stop_confirm:      ['custom_args'],
    admin_network_change:   ['latitude', 'longitude', 'wan_ip', 'custom_args'],
    admin_dual_eligability: ['eligibilities', 'custom_args'],
}

#11 01 00 1D 26 76 4B 01 00 00 00 1E 00 09 4F 4F 54 4E 2E 54 69 6D 65 72 43 6F 6E 66 69 72 6D 61 74 69 6F 6E 00 06 03 3C 00 04 00 85 27
#11 00 00 1D 26 76 4B 01 00 00 00 1C 00 09 4F 4F 54 4E 2E 54 69 6D 65 72 43 6F 6E 66 69 72 6D 61 74 69 6F 6E 00 06 03 3C 00 8F EA
argP = namedtuple('argumentParams',['help','type','choices','default'])
""" Describes the field, all are optional """
field_descriptions = {
#    'message_type':     {'help': "Message Type",                        'type': int,  'default': "dual avl", 'choices': message_format_handlers},
    'file':             {'help': "Location of the test file",           'type': str,  'default': "/Users/keenan/Desktop/Projects/TOGS_UDP_Sender-master/sample_data.csv"},
    'host':             {'help': "Hostname or IP of Backend",           'type': str,  'default': "66.244.232.186"}, # avl.ac05.com | 66.244.232.186 <= avl.geotracdemo.com
    'port':             {'help': "Backend port",                        'type': int,  'default': 6110},
    'esn':              {'help': "ESN",                                 'type': int,  'default': 5571001222}, # 5571001092 -> broken | 5571001222 -> Jack5530LT | 5561001501 -> Daniel5530
    'latitude':         {'help': "Latitude in decimal",                 'type': str,  'default': "51.1"},
    'longitude':        {'help': "Longitude in decimal",                'type': str,  'default': "-113"},
    'speed':            {'help': "Speed in km/h",                       'type': int,  'default': 20},
    'event_id':         {'help': "Event ID",                            'type': int,  'default': 1},
    'seqno':            {'help': "Sequence Number of Message",          'type': int,  'default': 1},
    'rssi':             {'help': "Unsigned Negative Value",             'type': int,  'default': 60},
    'heading':          {'help': "Heading",                             'type': int,  'default': 90},
    'odo':              {'help': "Odometer Value",                      'type': int,  'default': 341297},
    'timer':            {'help': "Timer for OOTN",                      'type': int,  'default': 5},
    'eligibilities':    {'help': "Comma separated, [0-5]",              'type': str,  'default': "0,0,0,0,0,0"},
    'wan_ip':           {'help': "IP address, or 'none' for Iridium",   'type': str,  'default': "123.45.67.89"},
    'custom_args':      {'help': "Wrap in a Named Payload message?",    'type': str,  'default': "none"},
}

""" Structure of message arguments constructed by getting keys from defaults,
    only esn and  seqno are required
"""
menuOnly = [ "message_type", "host", "port" ]

#TODO: Get rid of the namedtuple stuff
Command = namedtuple('Command', 
    [ i for i in [*field_descriptions] if i not in menuOnly ], 
    defaults = (None,) * (len([*field_descriptions]) - len(menuOnly) + 1) #[ None for i in field_descriptions if i not in menuOnly]
)


def handle_single(host, port, message_type, args,lc = 1, filename="NONE"):
    try:
        if message_type not in message_format_handlers:
            raise Exception(f'Invalid message type {message_type}\nargs:{",".join(args)}')

        generate_message = message_format_handlers.get(message_type)
        message = generate_message(args)

        extra_log = f' line {lc} from {filename}\n' if filename != "NONE" else ""

        log.info(f"Sending {extra_log}{message}")

        #print(args.esn,message,sep="\n")
        #print(bytes.fromhex(message))
        response = send_udp(host, port, message)

        if len(response) > 0:
            log.info("Response:")
            log.info(response)
            if (message_type not in [ bluetree, calamp ]):
                log.info(umf_parse_response(response))
        else:
            log.info("No Response")

        return response
    except Exception as e:
        print(e)
        return ''


def handle_csv(args, seqno):
    host = args.host
    port = args.port
    message_type = args.message_type
    filename = args.file

    column_names = {}
    with open(filename) as csv_file:
        lc = 0
        csv_reader = csv.reader(csv_file)

        for row in csv_reader:
            if lc == 0:
                for col_index in range(0, len(row)):
                    column_names[row[col_index]] = col_index
            else:
                #TODO: make this work with kwargs or something
                single_command_args = Command(
                    esn = int(row[ column_names["esn"] ]),
                    latitude = row[ column_names["latitude"] ],
                    longitude = row[ column_names["longitude"] ],
                    speed = int(row[ column_names["speed"] ]),
                    eventid = int(row[ column_names["eventid"] ]),
                    seqno = seqno,
                    rssi = 10,
                    heading = 10,
                    odo = 10
                )
                handle_single(host,port,message_type,single_command_args)
            lc = lc + 1
            seqno = seqno + 1
            sleep(2)

@Gooey(default_size=(800, 700),
       advanced=True,
       dump_build_config=True,
       program_name='TOGS UDP Sender',
       show_restart_button=False,
       navigation='SIDEBAR',
       show_sidebar=True,
       sidebar_title='message_type',
       show_success_modal=False,
       show_stop_warning=False,
       terminal_font_family='monospace'
       )
def main():
    parser = GooeyParser(description="Send Bluetree and Calamp UDP Messages")

    subparsers = parser.add_subparsers(dest="message_type")

    # Add message type
    for mtype, fields in message_format_fields.items():
        subparser = subparsers.add_parser(mtype)
        # Add arguments for field
        for field in all_formats_fields + fields:
            kwargs = field_descriptions[field]
            if ('optional' in kwargs):
                del kwargs['optional']
                subparser.add_argument('-' + field,field, **kwargs)
            else:
                subparser.add_argument(field, **kwargs)


    # single_parser = subparsers.add_parser("single", help="Sends a single UDP message")
    # for key, value in defaults:
    #     single_parser.add_argument(key, **value)
    # single_parser.add_argument("message_type", help="Message Type", type=str, choices=message_formats, default=defaults["message_type"])
    # single_parser.add_argument("host", help="Hostname or IP address of Backend", type=str, default=defaults["host"])
    # single_parser.add_argument("port", help="Backend port", type=int, default=defaults["port"])
    # single_parser.add_argument("esn", help="ESN", type=int, default=defaults["esn"])
    # single_parser.add_argument("latitude", help="Latitude in decimal", type=str, default=defaults["latitude"])
    # single_parser.add_argument("longitude", help="Longitude in decimal", type=str, default=defaults["longitude"])
    # single_parser.add_argument("speed", help="Speed in km/h", type=int, default=defaults["speed"])
    # single_parser.add_argument("event_id", help="Event ID", type=int, default=defaults["event_id"])

    # csv_parser = subparsers.add_parser("csv", help="Sends multiple UDP messages based on CSV file")
    # csv_parser.add_argument("message_type", help="Message Type", type=str, choices=message_formats)
    # csv_parser.add_argument("host", help="Hostname or IP address of Backend", type=str, default=defaults["host"])
    # csv_parser.add_argument("port", help="Backend port", type=int, default=defaults["port"])
    # csv_parser.add_argument("file", help="Filename", widget='FileChooser', default=defaultFile)

    args = parser.parse_args()
    kwargs = dict([(key,val) for key, val in args.__dict__.items() if key in Command._fields])
    #print(args)
    if args.message_type == 'csv':
        log.debug("CSV mode")
        handle_csv( args , args.seqno)
    else:
        single_command_args = Command(**kwargs)
        handle_single( args.host,
                       args.port,
                       args.message_type,
                       single_command_args )

    # if args.send_mode == 'single':
    #     log.debug("Single Message mode")
    #     single_command_args = Command(**args)
    #     # single_command_args = Command( esn = args.esn,
    #     #                                latitude = args.latitude,
    #     #                                longitude = args.longitude,
    #     #                                speed = args.speed,
    #     #                                eventid = args.event_id,
    #     #                                seqno=seqno,
    #     #                                rssi = 10,
    #     #                                heading = 10,
    #     #                                odo = 10 )
    #     handle_single( args.host,
    #                    args.port,
    #                    args.message_type,
    #                    single_command_args )
    # elif args.send_mode == 'csv':
    #     log.debug("CSV mode")
    #     handle_csv( args , seqno)


if __name__ == "__main__":
    main()
