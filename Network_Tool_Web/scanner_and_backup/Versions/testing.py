from snmpmod import SnmpGet


hosts = '172.31.240.138 '

mikrotik_identity = 'iso.3.6.1.2.1.1.5.0'
mikrotik_version = 'iso.3.6.1.2.1.47.1.1.1.1.2.65536'
mikrotik_model = 'iso.3.6.1.2.1.1.1.0'
mikrotik_serial = '1.3.6.1.4.1.14988.1.1.7.3.0'


def get_mk_name():
    SnmpGet(host=hosts, oid=mikrotik_identity)


def get_mk_version():
    SnmpGet(host=hosts, oid=mikrotik_version)


def get_mk_model():
    SnmpGet(host=hosts, oid=mikrotik_model)


def get_mk_serial():
    SnmpGet(host=hosts, oid=mikrotik_serial)


if __name__ == '__main__':
    get_mk_name()
    get_mk_model()
    get_mk_version()
    get_mk_serial()
