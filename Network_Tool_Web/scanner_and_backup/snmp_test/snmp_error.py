from pysnmp.entity.rfc3413.oneliner import cmdgen

mikrotik_identity = 'iso.3.6.1.2.1.1.5.0'
mikrotik_version = 'iso.3.6.1.2.1.47.1.1.1.1.2.65536'
mikrotik_model = 'iso.3.6.1.2.1.1.1.0'
mikrotik_serial = '1.3.6.1.4.1.14988.1.1.7.3.0'


class SnmpGet:

    def __init__(self, hosts, oid):

        self.hosts = hosts
        self.oid = oid

        snmp_gen = cmdgen.CommandGenerator()

        errorindication, errorstatus, errorindex, varbinds = snmp_gen.getCmd(
            cmdgen.CommunityData('publ1c'),
            cmdgen.UdpTransportTarget(('172.31.16.17', 161)), mikrotik_identity)

        for name, val in varbinds:
            print(val)
