from snmpmod import SnmpGet


hosts = '172.31.240.130'

mikrotik_identity = 'iso.3.6.1.2.1.1.5.0'
mikrotik_version = 'iso.3.6.1.2.1.47.1.1.1.1.2.65536'
mikrotik_model = 'iso.3.6.1.2.1.1.1.0'
mikrotik_serial = '1.3.6.1.4.1.14988.1.1.7.3.0'
snmp_community = 'publ1c'


name = str(SnmpGet(host=hosts, oid=mikrotik_identity, community=snmp_community))


if __name__ == '__main__':

    print(name)
#    print(SnmpGet(host=hosts, oid=mikrotik_identity, community=snmp_community)
#    SnmpGet(host=hosts, oid=mikrotik_model, community=snmp_community)
#    SnmpGet(host=hosts, oid=mikrotik_version, community=snmp_community)
#    SnmpGet(host=hosts, oid=mikrotik_serial, community=snmp_community)
