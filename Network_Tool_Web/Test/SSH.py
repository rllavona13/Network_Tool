import paramiko
import json
import nmap

# Json reader
config_file = open('auth.json')
config = json.load(config_file)
config_file.close()
# ip = '172.31.240.133'


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
                        mikrotik_hosts = host

                        print(host)  # print the ip which are trying to connect.
                        try:
                            ssh = paramiko.SSHClient()
                            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                            ssh.connect(hostname=ip, username=config['username'], password=config['password'])
                            ssh.invoke_shell()
                            stdin, stdout, stderr = ssh.exec_command('system identity print\n' 
                                                                     'system routerboard print\n' 
                                                                     'ip address print')
                            print(stdout.read())
                            ssh.close()

                        except Exception as ex:  # print the error and continues with the next ip address
                            print(ex)


if __name__ == '__main__':
    Scanner(host='172.31.240.0/24')
