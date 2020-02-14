from string import Template


frame_start = 'AA 55 '              # Message Frame Start (constant)
frame_end = 'C9 17 '                # Message Frame End (constant)

#   bep
#####################
bep_header = Template(
    '$imei 00 01 01 01 $seqno $length $eventid 00 00 50 11 '
)

bep_body = Template(
    '01 A0 $gp1 04 55 A9 F8 05 04 DC 3A 1D D1 '
)


#   lmdirect
#####################
lmdirect = Template(
    '83 05 $esn 01 01 01 02 $seqno $timestamp1 $timestamp2 $coordinates $speed 00 0E 08 00 00 00 00 00 0F 0A 01 00 FF $eventid 01 00 01 97 21 C9'
)


#   umf
#####################
umf_header = Template(
    '11 $seq $esn $len'
)

umf = Template(
    '$header $body $chksum'
)

umf_named_payload = Template(
    '09 $name $body $len'
)


#   umf functions
#####################
umf_dual_AVL = Template(
    '01 $eventid $gps_timestamp $rssi $speed $heading $odo'
)

umf_ootn = Template(
    '06 $type $args'
)


#   administration
#####################

umf_admin_dual_mode_elig = Template(
    '00 00 $time 06 $admin $avl $ecm $garmin $ibutton $psm'
)

umf_admin_dual_mode_usage = Template(
    '00 01 $time $month $year $max_bytes $out_bytes $in_bytes'
)

umf_admin_usage_limit_reached = Template(
    '00 02 $time $max_bytes $out_bytes $in_bytes'
)

umf_admin_iridium_link_check = Template(
    '00 03 $time $imei $err0 $err1 $err2 $lenFV $FirmVersion'
)

umf_admin_net_medium_change = Template(
    '00 04 $gps $netM $size $ip'
)
