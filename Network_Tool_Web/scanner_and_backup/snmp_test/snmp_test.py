from pysnmp.entity.rfc3413.oneliner import cmdgen

host = '172.31.240.133' \
       ''
def get_identity():

    # host = '172.31.240.133'

    snmp_gen = cmdgen.CommandGenerator()

    mikrotik_identity = 'iso.3.6.1.2.1.1.5.0'

    errorindication, errorstatus, errorindex, varbinds = snmp_gen.getCmd(
        cmdgen.CommunityData('public'),
        cmdgen.UdpTransportTarget(((host), 161)), mikrotik_identity)

    for name, val in varbinds:
        device_name = val

def get_version():

    # host = '172.31.240.133'

    snmp_gen = cmdgen.CommandGenerator()

    mikrotik_version = 'iso.3.6.1.2.1.47.1.1.1.1.2.65536'

    errorindication, errorstatus, errorindex, varbinds = snmp_gen.getCmd(
        cmdgen.CommunityData('public'),
        cmdgen.UdpTransportTarget(((host), 161)), mikrotik_version)

    for name, val in varbinds:
        print(val)


def get_model():

    # host = '172.31.240.133'

    snmp_gen = cmdgen.CommandGenerator()

    mikrotik_model = 'iso.3.6.1.2.1.1.1.0'

    errorindication, errorstatus, errorindex, varbinds = snmp_gen.getCmd(
        cmdgen.CommunityData('public'),
        cmdgen.UdpTransportTarget(((host), 161)), mikrotik_model)

    for name, val in varbinds:
        print(val)


if __name__ == "__main__":

    print("Name: ", get_identity())
    print("Model: ", get_model())
    print("RouterOS Version :", get_version())
