import sys
import paramiko
import json
import nmap
import mysql.connector


config_file = open('/home/rrivera/Documents/Python_Projects/Network_Tool/Network_Tool_Web/Test/auth.json')
config = json.load(config_file)
config_file.close()


class Scanner:

    def __init__(self, host):

        self.host = host
        self.nmscanner = nmap.PortScanner()
        self.nmscanner.scan(hosts=host, arguments='-Pn -p 8291 --ttl 10 --max-retries 1')

        for host in self.nmscanner.all_hosts():

            for proto in self.nmscanner[host].all_protocols():

                lport = list(self.nmscanner[host][proto].keys())
                lport.sort()

                for port in lport:
                    list_ports = (port, self.nmscanner[host][proto][port]['state'])

                    if list_ports[1] == 'open':
                        mk_list = host

                        print("%s Is a Mikrotik" % host)  # print the ip which are trying to connect.
                        print("")

                        try:
                            ssh = paramiko.SSHClient()
                            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                            ssh.connect(hostname=mk_list, username=config['username'], password=config['password'])
                            ssh.invoke_shell()
                            stdin, stdout, stderr = ssh.exec_command('system identity print')
                            mk_scanned_host = stdout.read()  # saves the output from ssh for MySQL query use
                            list_fixed = mk_scanned_host.strip('name:').split('name:')
                            identity_fixed = (list_fixed[1])
                            # print(json.dumps(mk_scanned_host, indent=4))
                            ssh.close()

                            sql_connector = mysql.connector.connect(user='python',
                                                                    password='yzh8RB0Bcw1VivO3',
                                                                    host='localhost',
                                                                    database='test')

                            cursor = sql_connector.cursor()

                            add_mikrotik = ("INSERT INTO devices"
                                            "(name, ip)"
                                            "VALUES ('%s', '%s')" % (identity_fixed, mk_list))

                            cursor.execute(add_mikrotik)
                            sql_connector.commit()
                            cursor.close()
                            sql_connector.close()
                            print(str(identity_fixed))
                            print("%s successfully added to the Mikrotik Database. " % host)

                            print('-------------------------------------------------------------')
                            print('')

                        except Exception as ex:  # print the error and continues with the next ip address
                            print(ex)

"""
SELECT EXISTS(SELECT 1 FROM devices WHERE ip='172.31.16.17') meter esto para verificar si un IP existe antes del add.
"""

if __name__ == '__main__':

    print('Scanning for Mikrotik Routers, your host/range is: %s' % sys.argv[1])
    print('')
    Scanner(host=sys.argv[1])
