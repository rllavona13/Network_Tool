__AUTHOR__ = 'Ramon Rivera Llavona'
__VERSION__ = 'Beta 1.6'

import nmap
import paramiko
from paramiko import AuthenticationException
from pysnmp.entity.rfc3413.oneliner import cmdgen
import mysql.connector
import sys
import json


config_file = open('auth.json')
auth = json.load(config_file)
config_file.close()


class Scanner:

    def __init__(self, host):

        self.host = host
        self.nmscanner = nmap.PortScanner()
        self.nmscanner.scan(hosts=host, arguments='-Pn -p 8291')

        for host in self.nmscanner.all_hosts():

            for proto in self.nmscanner[host].all_protocols():

                lport = list(self.nmscanner[host][proto].keys())
                lport.sort()

                for port in lport:
                    list_ports = (port, self.nmscanner[host][proto][port]['state'])

                    if list_ports[1] == 'open':
                        port = 22
                        nbytes = 4096

                        """
                        Configurations when connected to a mikrotik, it configures 
                        radius, add VPN ip addresses to the firewall,
                        configure a SNMP community and set it as active community
                        """
                        text_backup = 'export file=' + host
                        basic_backup = 'system backup save name=' + host
                        add_snmp_community = 'snmp community add name=publ1c ' \
                                             'read-access=yes addresses=196.12.161.0/24,192.168.253.0/24'
                        set_snmp_community = 'snmp set trap-community=publ1c trap-version=2'
                        add_radius = 'radius add address=196.12.161.54 secret=MikRadius service=login'
                        add_vpn_address_firewall = ' ip firewall address-list add list=Worldnet address=192.168.253.0/4'
                        set_use_radius = 'user aaa set use-radius=yes'

                        # Username and Passwords - Stored in JSON File called auth.json
                        radius_user = auth['username']
                        radius_password = auth['password']
                        xarxa_user = auth['other_username']
                        xarxa_password = auth['other_password']
                        mik277_user = auth['mik_username']
                        mik277_password = auth['mik_password']

                        if paramiko.AuthenticationException:
                            try:
                                client = paramiko.Transport(host, port)

                                client.connect(username=mik277_user, password=mik277_password)

                                stdout_data = []
                                stderr_data = []

                                session = client.open_channel(kind='session')
                                session.exec_command(add_snmp_community)
                                session = client.open_channel(kind='session')
                                session.exec_command(set_snmp_community)
                                session = client.open_channel(kind='session')
                                session.exec_command(add_vpn_address_firewall)
                                session = client.open_channel(kind='session')
                                session.exec_command(add_radius)
                                session = client.open_channel(kind='session')
                                session.exec_command(set_use_radius)
                                session = client.open_channel(kind='session')
                                session.exec_command(text_backup)
                                session = client.open_channel(kind='session')
                                session.exec_command(basic_backup)

                                print('')
                                print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
                                print('Please wait... Configuring SNMP Community in the system...')
                                print('Please wait... Creating %s' % host + '.rsc Backup in the Mikrotik File System')
                                print(
                                            'Please wait... Creating %s' % host +
                                            '.backup Backup in the Mikrotik File System')
                                print('')
                                print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
                                print('Backup successfully created at the File system')
                                print('')
                                print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
                                print('Please Wait, Gathering device information...')
                                print('')

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
                                    print('')
                                    print('Sorry try again...')
                                    print('')
                                client.close()

                            except paramiko.AuthenticationException:

                                client = paramiko.Transport(host, port)

                                client.connect(username=radius_user, password=radius_password)

                                stdout_data = []
                                stderr_data = []

                                session = client.open_channel(kind='session')
                                session.exec_command(add_snmp_community)
                                session = client.open_channel(kind='session')
                                session.exec_command(set_snmp_community)
                                session = client.open_channel(kind='session')
                                session.exec_command(add_vpn_address_firewall)
                                session = client.open_channel(kind='session')
                                session.exec_command(add_radius)
                                session = client.open_channel(kind='session')
                                session.exec_command(set_use_radius)
                                session = client.open_channel(kind='session')
                                session.exec_command(text_backup)
                                session = client.open_channel(kind='session')
                                session.exec_command(basic_backup)

                                print('')
                                print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
                                print('Please wait... Configuring SNMP Community in the system...')
                                print('Please wait... Creating %s' % host + '.rsc Backup in the Mikrotik File System')
                                print(
                                            'Please wait... Creating %s' % host +
                                            '.backup Backup in the Mikrotik File System')
                                print('')
                                print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
                                print('Backup successfully created at the File system')
                                print('')
                                print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
                                print('Please Wait, Gathering device information...')
                                print('')

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
                                    print('')
                                    print('Sorry try again...')
                                    print('')
                                client.close()

                        else:
                            client = paramiko.Transport(host, port)

                            client.connect(username=xarxa_user, password=xarxa_password)

                            stdout_data = []
                            stderr_data = []

                            session = client.open_channel(kind='session')
                            session.exec_command(add_snmp_community)
                            session = client.open_channel(kind='session')
                            session.exec_command(set_snmp_community)
                            session = client.open_channel(kind='session')
                            session.exec_command(add_vpn_address_firewall)
                            session = client.open_channel(kind='session')
                            session.exec_command(add_radius)
                            session = client.open_channel(kind='session')
                            session.exec_command(set_use_radius)
                            session = client.open_channel(kind='session')
                            session.exec_command(text_backup)
                            session = client.open_channel(kind='session')
                            session.exec_command(basic_backup)

                            print('')
                            print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
                            print('Please wait... Configuring SNMP Community in the system...')
                            print('Please wait... Creating %s' % host + '.rsc Backup in the Mikrotik')
                            print('Please wait... Creating %s' % host + '.backup Backup in the Mikrotik')
                            print('Please wait... Creating SNMP Community')
                            print('Please wait... Adding VPN IP Range into firewall address list')
                            print('')
                            print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
                            print('Backup successfully created at the File system')
                            print('')
                            print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
                            print('Please Wait, Gathering device information...')
                            print('')

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
                                print('')
                                print('Sorry try again...')
                                print('')
                            client.close()

                        class GetIdentity:

                            def __init__(self):
                                pass

                            # host = '172.31.240.133'

                            snmp_gen = cmdgen.CommandGenerator()

                            mikrotik_identity = 'iso.3.6.1.2.1.1.5.0'

                            values = errorindication, errorstatus, errorindex, varbinds = snmp_gen.getCmd(
                                cmdgen.CommunityData('publ1c'),
                                cmdgen.UdpTransportTarget(((host), 161)), mikrotik_identity)

                            for name, val in varbinds:
                                device_name = val

                        class GetVersion:

                            def __init__(self):
                                pass

                            # host = '172.31.240.133'

                            snmp_gen = cmdgen.CommandGenerator()

                            mikrotik_version = 'iso.3.6.1.2.1.47.1.1.1.1.2.65536'

                            values = errorindication, errorstatus, errorindex, varbinds = snmp_gen.getCmd(
                                cmdgen.CommunityData('publ1c'),
                                cmdgen.UdpTransportTarget(((host), 161)), mikrotik_version)

                            for name, val in varbinds:
                                device_version = val

                        class GetModel:

                            def __init__(self):
                                pass

                            # host = '172.31.240.133'

                            snmp_gen = cmdgen.CommandGenerator()

                            mikrotik_model = 'iso.3.6.1.2.1.1.1.0'

                            values = errorindication, errorstatus, errorindex, varbinds = snmp_gen.getCmd(
                                cmdgen.CommunityData('publ1c'),
                                cmdgen.UdpTransportTarget(((host), 161)), mikrotik_model)

                            for name, val in varbinds:
                                device_model = val

                        identity = str(GetIdentity.device_name)
                        version = str(GetVersion.device_version)
                        model = str(GetModel.device_model)
                        ip = str(host)

                        print('DEVICE INFO:')
                        print('IP Address: ' + host)
                        print('Name: ' + identity)
                        print('RouterOS Version: ' + version)
                        print('Mikrotik Model: ' + model)
                        print('By: Ramon Rivera - Neo Data')
                        print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')

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


if __name__ == '__main__':
    # Scanner(host=sys.argv[1])
    Scanner(host='172.31.240.133')
    print("")
