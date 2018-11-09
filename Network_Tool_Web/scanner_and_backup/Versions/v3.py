__AUTHOR__ = 'Ramon Rivera Llavona'
__VERSION__ = 'Beta 1.3'

"""
Trying to send via Paramiko for every host that are scanned and is a Mikrotik, create a backup,
but i have to find the way to iterate host by host and send the two types of backups. Also save the list of MK 
host scanned in a text file or Database(BEST)


Variables for the two commands are:

text_backup = 'export file=' + hosts
basic_backup = 'system backup save name=' + hosts

Version Beta 1.2

This version includes:

-JSON for Radius Authentication
-Paramiko Connection for SSH and send the backup commands.
-Takes arguments for running in the shell with given IP ex. python scanner.py 172.31.240.133

Version Beta 1.3

-Implemented both backup file. .rsc and .backup

Still working in order to implement error handling and other things

This version includes:

Note to myself: USE CLASSES FOR THIS!!

"""

import nmap
import json
import paramiko
import sys

config_file = open('auth.json')
auth = json.load(config_file)
config_file.close()


# scan para identificar Mikrotiks en la red y crear backup
def scanner(hosts):

    nscan = nmap.PortScanner()

    # hosts = '172.31.240.0/24'
    nscan.scan(hosts=hosts, arguments='-Pn -p 8291')

    for host in nscan.all_hosts():

        for proto in nscan[host].all_protocols():

            lport = list(nscan[host][proto].keys())
            lport.sort()

            for port in lport:
                list_ports = (port, nscan[host][proto][port]['state'])
                # print(host, list_ports)

                if list_ports[1] == 'open':

                    print("This host: %s is a Mikrotik" % host)
                    print("")
                    print("Please wait, Creating %s" % host + ".rsc, Backup in the Mikrotik File System")
                    print("")
                    print("Please wait, Creating %s" % host + ".backup, Backup in the Mikrotik File System")
                    print("")

                    file_name = host
                    f = open(file_name + '.txt', 'w')
                    f.write(host)
                    f.close()

                    # SSH Connection to Mikrotiks and send backups commands.
                    port = 22
                    nbytes = 4096

                    text_backup = 'export file=' + hosts
                    basic_backup = 'system backup save name=' + hosts

                    client = paramiko.Transport(hosts, port)
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
                        print("")
                        print("Backup successfully created at the File system")
                        print("")
                        client.close()
                    else:
                        print("")
                        print("Sorry try again...")
                        print("")
                        client.close()


if __name__ == '__main__':

    scanner('172.31.240.133')
    #scanner(sys.argv[1])
    print("")
    print("Created by Ramon Rivera Llavona")
    print("")