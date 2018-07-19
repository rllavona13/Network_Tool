"""
This module scan specifically for port 8291 which is RouterOS default port for Management UI Winbox.
If is a match it will create a list object of hosts that are devices mikrotik called _isMK.

"""

import nmap


class MkScanner:

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

                    _isMK = []
                    if list_ports[1] == 'open':
                        _isMK.append([host])
                        print(_isMK)


# for testing
# MkScanner(host='172.31.240.0/24')
