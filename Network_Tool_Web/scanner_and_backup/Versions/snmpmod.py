from pysnmp.entity.rfc3413.oneliner import cmdgen


class SnmpGet:

    def __init__(self, host, oid):

        self.host = host
        self.oid = oid

        snmp_gen = cmdgen.CommandGenerator()

        errorindication, errorstatus, errorindex, varbinds = snmp_gen.getCmd(
            cmdgen.CommunityData('publ1c'),
            cmdgen.UdpTransportTarget(((host), 161)), self.oid)

        for name, val in varbinds:
            oid = val
            print(str(oid))
