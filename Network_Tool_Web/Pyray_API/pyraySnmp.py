"""
This module handles the SNMP get to the mikrotiks in order to retrieve, system identity, system version
and system model.

I have to create a test unit in order to test that it passes the Scanner host to the classes.

"""

from pysnmp.entity.rfc3413.oneliner import cmdgen


# Uses mikrotik OID for system identity
# Also verify how to use different SNMP Communities if one fail
class GetIdentity:

    def __init__(self, host):

        self.host = host
    # host = '172.31.240.133'

        snmp_gen = cmdgen.CommandGenerator()

        mikrotik_identity = 'iso.3.6.1.2.1.1.5.0'

        values = errorindication, errorstatus, errorindex, varbinds = snmp_gen.getCmd(
            cmdgen.CommunityData('publ1c'),
            cmdgen.UdpTransportTarget(((host), 161)), mikrotik_identity)

        for name, val in varbinds:
            device_name = val


# Uses mikrotik OID for system version
# Also verify how to use different SNMP Communities if one fail
class GetVersion:

    def __init__(self, host):

        self.host = host

    # host = '172.31.240.133'

        snmp_gen = cmdgen.CommandGenerator()

        mikrotik_version = 'iso.3.6.1.2.1.47.1.1.1.1.2.65536'

        values = errorindication, errorstatus, errorindex, varbinds = snmp_gen.getCmd(
            cmdgen.CommunityData('publ1c'),
            cmdgen.UdpTransportTarget(((host), 161)), mikrotik_version)

        for name, val in varbinds:
            device_version = val


# Uses mikrotik OID for Router Model
# Also verify how to use different SNMP Communities if one fail
class GetModel:

    def __init__(self, host):
        self.host = host

        # host = '172.31.240.133'

        snmp_gen = cmdgen.CommandGenerator()

        mikrotik_model = 'iso.3.6.1.2.1.1.1.0'

        values = errorindication, errorstatus, errorindex, varbinds = snmp_gen.getCmd(
            cmdgen.CommunityData('publ1c'),
            cmdgen.UdpTransportTarget(((host), 161)), mikrotik_model)

        for name, val in varbinds:
            device_model = val
