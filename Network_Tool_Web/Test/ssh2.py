import paramiko
import json
import nmap
import mysql.connector
import sys


config_file = open('auth.json')
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

                        print("IP Address of Mikrotik is %s" % host)  # print the ip which are trying to connect.
                        print("")

                        try:
                            ssh = paramiko.SSHClient()
                            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                            ssh.connect(hostname=mk_list, username=config['username'], password=config['password'])
                            ssh.invoke_shell()
                            stdin, stdout, stderr = ssh.exec_command('system identity print')

                            mk_scanned_host = stdout.read()  # saves the output from ssh for MySQL query use

                            list_fixed = mk_scanned_host.strip('name:').split('name:')  # Here we "cut off" name: from strings.
                                                                             # Leaving only the name
                            identity_fixed = (list_fixed[1])
                            # print(json.dumps(mk_scanned_host, indent=4))
                            print(str(identity_fixed))
                            print("==============================================================================")
                            ssh.close()

                            f = open('mikrotik_list.txt', 'a')
                            f.write(str(str(identity_fixed) + mk_list))


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

                        except Exception as ex:  # print the error and continues with the next ip address
                            print(ex)

                            open('mikrotik_list.txt', 'a')
                            f.write(ex)
                            f.close()



if __name__ == '__main__':
    Scanner(host='172.31.242.0/24')
    # Scanner(host=sys.argv[1])
