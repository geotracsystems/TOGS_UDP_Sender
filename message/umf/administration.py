
"""

   message.umf.administration.dual_mode_eligibility
   message.umf.administration.dual_mode_usage
   message.umf.administration.monthly_data_limit_reached
   message.umf.administration.iridium_link_check
   message.umf.administration.network_medium_change

"""
from message.umf import umf_wrap_body, umf_named_payload, umf_gps_time, message_template, sized_hex, umf_time, umf_ip

'''
    0: MINIMAL
    1: LOW
    2: MEDIUM
    3: HIGH
    4: MAXIMUM
    5: CELL_ONLY
'''


def dual_mode_eligibility(args):
    ''' '00 00 $time 06 $admin $avl $ecm $garmin $ibutton $psm' '''
    eligibilities = args.eligibilities.split(',')
    body = message_template.umf_admin_dual_mode_elig.substitute(
            time = umf_time(),
            admin = sized_hex(eligibilities[0],1),
            avl = sized_hex(eligibilities[1],1),
            ecm = sized_hex(eligibilities[2],1),
            garmin = sized_hex(eligibilities[3],1),
            ibutton = sized_hex(eligibilities[4],1),
            psm = sized_hex(eligibilities[5],1),
        )
    #if ('-named' in args.custom_args):
     #   body = umf_named_payload(body,'Dual-ModeEligibility')

    return umf_wrap_body(
        body, args.esn, args.seqno
    )


def dual_mode_usage(args):
    raise NotImplementedError()
    ''' '00 01 $time $month $year $max_bytes $out_bytes $in_bytes' '''
    body = message_template.umf_admin_dual_mode_usage.substitute(
            time = umf_time(),
            month = '',
            year = '',
            max_bytes = '',
            out_bytes = '',
            in_bytes = ''
        )
    if ('-named' in args.custom_args):
        body = umf_named_payload(body,'Dual-ModeUsage')

    return umf_wrap_body(
        body, args.esn, args.seqno
    )


def monthly_data_limit_reached(args):
    raise NotImplementedError()
    ''' '00 02 $time $max_bytes $out_bytes $in_bytes' '''
    body = message_template.umf_admin_usage_limit_reached.substitute(
            
        )
    if ('-named' in args.custom_args):
        body = umf_named_payload(body,'MonthlyDataLimitReached')

    return umf_wrap_body(
        body, args.esn, args.seqno
    )


def iridium_link_check(args):
    raise NotImplementedError()
    ''' '00 03 $time $imei $err0 $err1 $err2 $lenFV $FirmVersion' '''
    body = message_template.umf_admin_iridium_link_check.substitute(
            
        )
    if ('-named' in args.custom_args):
        body = umf_named_payload(body,'Iridium-Link-Check')

    return umf_wrap_body(
        body, args.esn, args.seqno
    )


def network_medium_change(args):
    ''' '00 04 $gps $netM $size $ip' '''
    cellular = len(args.wan_ip) > 0
    body = message_template.umf_admin_net_medium_change.substitute(
            gps = umf_gps_time(args.latitude, args.longitude),
            netM = sized_hex(0 if cellular else 1, 1),
            size = sized_hex(4 if cellular else 0, 1),
            ip = umf_ip(args.wan_ip) if cellular else ''
        )

    if ('-named' in args.custom_args):
        body = umf_named_payload(body,'Network-Medium-Change')

    return umf_wrap_body(
        body, args.esn, args.seqno
    )
