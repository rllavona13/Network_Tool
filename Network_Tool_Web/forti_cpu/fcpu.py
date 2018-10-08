from pysnmp.entity.rfc3413.oneliner import cmdgen
import time


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
            fortinet_cpu = val
            print('')
            print('Fortinet 800c CPU: %s' % fortinet_cpu)


if __name__ == '__main__':

    SnmpGet(host='196.12.161.1', oid='1.3.6.1.4.1.12356.101.4.1.3.0', community='c4ct1!')
