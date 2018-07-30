from pysnmp.entity.rfc3413.oneliner import cmdgen


class SnmpGet:

    def __init__(self, host, oid, community):

        self.host = host
        self.oid = oid
        self.community = community

        snmp_gen = cmdgen.CommandGenerator()

        errorindication, errorstatus, errorindex, varbinds = snmp_gen.getCmd(
            cmdgen.CommunityData(self.community),
            cmdgen.UdpTransportTarget(((self.host), 161)), self.oid)

        for name, val in varbinds:
            oid = val
            print(str(oid))

    def version(self, host, oid, community):

        self.host = host
        self.oid = oid
        self.community = community

        snmp_gen = cmdgen.CommandGenerator()

        errorindication, errorstatus, errorindex, varbinds = snmp_gen.getCmd(
            cmdgen.CommunityData(self.community),
            cmdgen.UdpTransportTarget(((self.host), 161)), self.oid)

        for name, val in varbinds:
            oid = val
            print(str(oid))

