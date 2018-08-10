__AUTHOR__ = 'Ramon Rivera Llavona'
__VERSION__ = 'Beta 1.0'

"""
This is the first and basic app, it scan a network and based if the port 9291 which is Winbox is open
and print the hosts that are Mikrotik.

The idea is use the list of Mikrotik hosts and using SSH or MK API create backups automatically

"""

import nmap
import sys
from pysnmp.entity.rfc3413.oneliner import cmdgen


mikrotik_identity = 'iso.3.6.1.2.1.1.5.0'
mikrotik_version = 'iso.3.6.1.2.1.47.1.1.1.1.2.65536'
mikrotik_model = 'iso.3.6.1.2.1.1.1.0'
mikrotik_serial = '1.3.6.1.4.1.14988.1.1.7.3.0'


# scan para identificar Mikrotiks en la red
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
                    #  mk_lst = ("This host: %s is a Mikrotik" % host)
                    mk_lst = host
                    print(mk_lst)


if __name__ == '__main__':


    scanner(hosts='172.31.240.0/24')
    # scanner(sys.argv[1])
    print("")
