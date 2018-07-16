import nmap
import json
import paramiko
import sys
import mysql.connector
from datetime import time
from pysnmp.hlapi import ObjectIdentity, ContextData, Integer, OctetString
from pysnmp.hlapi import SnmpEngine, setCmd, CommunityData, UdpTransportTarget, ObjectType
from pysnmp.entity.rfc3413.oneliner import cmdgen
from pprint import pprint


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
                        print("This Device: %s is a Mikrotik" % host)
                        print("")
                        print("Please wait... Creating %s" % host + ".rsc, Backup in the Mikrotik File System")
                        print("")
                        print("Please wait... Creating %s" % host + ".backup, Backup in the Mikrotik File System")
                        print("")

                        port = 22
                        nbytes = 4096

                        text_backup = 'export file=' + host
                        basic_backup = 'system backup save name=' + host

                        client = paramiko.Transport(host, port)
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
                            print("Backup successfully created at the File system")
                            print("")
                            client.close()
                        else:
                            print("")
                            print("Sorry try again...")
                            print("")
                            client.close()

                        class GetIdentity:

                            def __init__(self):
                                pass

                            # host = '172.31.240.133'

                            snmp_gen = cmdgen.CommandGenerator()

                            mikrotik_identity = 'iso.3.6.1.2.1.1.5.0'

                            values = errorindication, errorstatus, errorindex, varbinds = snmp_gen.getCmd(
                                cmdgen.CommunityData('public'),
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
                                cmdgen.CommunityData('public'),
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
                                cmdgen.CommunityData('public'),
                                cmdgen.UdpTransportTarget(((host), 161)), mikrotik_model)

                            for name, val in varbinds:
                                device_model = val

                        identity = str(GetIdentity.device_name)
                        version = str(GetVersion.device_version)
                        model = str(GetModel.device_model)
                        ip = str(host)



                        """
                        MySQL Connection and save to DB the scanned devices.
                        """

                        sql_connector = mysql.connector.connect(user='python',
                                                                password='0fz5AepAzg8LgK97',
                                                                host='localhost',
                                                                database='test')

                        devices = host
                        name = identity
                        serial = serial
                        model = model

                        cursor = sql_connector.cursor()

                        add_mikrotik = ("INSERT INTO devices "
                                        "(host, name, serial, model"
                                        "VALUES ( '%s', '%s', '%s', '%s')" % devices, name, serial, model)

                        cursor.execute(add_mikrotik)
                        sql_connector.commit()
                        cursor.close()
                        sql_connector.close()


if __name__ == '__main__':

    # Scanner(host=sys.argv[1])
    Scanner(host='172.31.240.133')
    print("")
