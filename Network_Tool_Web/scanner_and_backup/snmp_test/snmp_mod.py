__AUTHOR__ = 'Ramon Rivera Llavona'
__VERSION__ = 'Beta 1.5'

import nmap
import paramiko
from pysnmp.entity.rfc3413.oneliner import cmdgen
import mysql.connector
import sys
import json

config_file = open('auth.json')
auth = json.load(config_file)
config_file.close()


def scanner(host):
    nmscanner = nmap.PortScanner()
    nmscanner.scan(hosts=host, arguments='-Pn -p 8291')

    for host in nmscanner.all_hosts():

        for proto in nmscanner[host].all_protocols():

            lport = list(nmscanner[host][proto].keys())
            lport.sort()

            for port in lport:
                list_ports = (port, nmscanner[host][proto][port]['state'])

                if list_ports[1] == 'open':
                    host = host
                    print(host)


def get_snmp_identity():
    # host = '172.31.240.133'

    snmp_gen = cmdgen.CommandGenerator()

    mikrotik_identity = 'iso.3.6.1.2.1.1.5.0'

    values = errorindication, errorstatus, errorindex, varbinds = snmp_gen.getCmd(
        cmdgen.CommunityData('public'),
        cmdgen.UdpTransportTarget(((scanner()), 161)), mikrotik_identity)

    for name, val in varbinds:
        device_name = val


def get_snmp_version():
    # host = '172.31.240.133'

    snmp_gen = cmdgen.CommandGenerator()

    mikrotik_version = 'iso.3.6.1.2.1.47.1.1.1.1.2.65536'

    values = errorindication, errorstatus, errorindex, varbinds = snmp_gen.getCmd(
        cmdgen.CommunityData('public'),
        cmdgen.UdpTransportTarget(((scanner()), 161)), mikrotik_version)

    for name, val in varbinds:
        device_version = val


class GetModel:

    def __init__(self):
        pass

    # host = '172.31.240.133'

    snmp_gen = cmdgen.CommandGenerator()

    mikrotik_model = 'iso.3.6.1.2.1.1.1.0'

    values = errorindication, errorstatus, errorindex, varbinds = snmp_gen.getCmd(
        cmdgen.CommunityData('public'),
        cmdgen.UdpTransportTarget(((scanner()), 161)), mikrotik_model)

    for name, val in varbinds:
        device_model = val


identity = str(GetIdentity.device_name)
version = str(GetVersion.device_version)
model = str(GetModel.device_model)
ip = str(scanner())

"""
def ssh_connection():
    print("")
    print("Please wait... Creating %s" % host + ".rsc Backup in the Mikrotik File System")
    print("Please wait... Creating %s" % host + ".backup Backup in the Mikrotik File System")
    print("")
    print("Backup successfully created at the File system")
    print("")
    print("Please Wait, Gathering device information...")

    port = 22
    nbytes = 4096

    text_backup = 'export file=' + host
    basic_backup = 'system backup save name=' + host

    client = paramiko.Transport(self.host, port)
    client.connect(username=auth['username'], password=auth['password'])

    stdout_data = []
    stderr_data = []

    session = client.open_channel(kind='session')
    session.exec_command(text_backup)
    session = client.open_channel(kind='session')
    session.exec_command(basic_backup)

    while True:
        if session.recv_ready():
            stdout_data.append(session.recv(nbytes))
        if session.recv_stderr_ready():
            stderr_data.append(session.recv_stderr(nbytes))
        if session.exit_status_ready():
            break

    session.close()
    if session.recv_exit_status() == 0:
        client.close()
    else:
        print("")
        print("Sorry try again...")
        print("")
        client.close()



    sql_connector = mysql.connector.connect(user='python',
                                            password='yzh8RB0Bcw1VivO3',
                                            host='localhost',
                                            database='MikrotikDB')
    cursor = sql_connector.cursor()
    add_mikrotik = ("INSERT INTO devices"
                    "(name, ip, model, version)"
                    "VALUES ('%s', '%s', '%s', '%s')" % (identity, ip, model, version))
    cursor.execute(add_mikrotik)
    sql_connector.commit()
    cursor.close()
    sql_connector.close()
"""

if __name__ == '__main__':
    # Scanner(host=sys.argv[1])
    scanner(host='172.31.240.0/24')

    print('')
    print('DEVICE INFO:')
    print('IP Address: ' + str(scanner()))
    print('Name: ' + identity)
    print('RouterOS Version: ' + version)
    print('Mikrotik Model: ' + model)