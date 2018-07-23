from pysnmp.entity.rfc3413.oneliner import cmdgen

try:

    host = '172.31.240.160'

    snmp_gen = cmdgen.CommandGenerator()
    mikrotik_identity = 'iso.3.6.1.2.1.1.5.0'

    values = errorindication, errorstatus, errorindex, varbinds = snmp_gen.getCmd(
        cmdgen.CommunityData('publ1c'),
        cmdgen.UdpTransportTarget(((host), 161)), mikrotik_identity)

    for name, val in varbinds:
        device_name = val

        identity = str(device_name)
        ip = str(host)

        print('DEVICE INFO:')
        print('IP Address: ' + host)
        print('Name: ' + identity)
        print('By: Ramon Rivera - Neo Data')
        print('+++++++++++++++++++++++++++++++++++++++++++++++++')

except:
    pass
