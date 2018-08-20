import paramiko
import json
import nmap
import mysql.connector
import sys
from multiprocessing import Process

config_file = open('auth.json')
config = json.load(config_file)
config_file.close()
# ip = '172.31.240.133'


class Scanner:

    def __init__(self, host):

        self.host = host
        self.nmscanner = nmap.PortScanner()
        self.nmscanner.scan(hosts=host, arguments='-Pn -p 8291 --min-hostgroup 256 --ttl 10 --max-retries 1')

        for host in self.nmscanner.all_hosts():

            for proto in self.nmscanner[host].all_protocols():

                lport = list(self.nmscanner[host][proto].keys())
                lport.sort()

                for port in lport:
                    list_ports = (port, self.nmscanner[host][proto][port]['state'])

                    if list_ports[1] == 'open':
                        mk_list = host

                        print("IP Address of Mikrotik is %s" % host)  # print the ip which are trying to connect.
                        print("")

                        try:
                            ssh = paramiko.SSHClient()
                            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                            ssh.connect(hostname=mk_list, username=config['username'], password=config['password'])
                            ssh.invoke_shell()
                            stdin, stdout, stderr = ssh.exec_command('system identity print')

                            mk_scanned_host = stdout.read()  # saves the output from ssh for MySQL query use
                            print(stdout.read())

                            print("==============================================================================")
                            ssh.close()

                            sql_connector = mysql.connector.connect(user='python',
                                                                    password='yzh8RB0Bcw1VivO3',
                                                                    host='localhost',
                                                                    database='test')

                            cursor = sql_connector.cursor()

                            add_mikrotik = ("INSERT INTO devices"
                                            "(name, ip)"
                                            "VALUES ('%s', '%s')" % (mk_scanned_host, mk_list))

                            cursor.execute(add_mikrotik)
                            sql_connector.commit()
                            cursor.close()
                            sql_connector.close()

                        except Exception as ex:  # print the error and continues with the next ip address
                            print(ex)


if __name__ == '__main__':
    Scanner(host='172.16.240.0/24')
    # Scanner(host=sys.argv[1])
