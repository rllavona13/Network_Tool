"""
This module scan specifically for port 8291 which is RouterOS default port for Management UI Winbox.
If is a match it will create a list object of hosts that are devices mikrotik called _isMK.

"""

import nmap
import mysql.connector


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

                    if list_ports[1] == 'open':
                        self.host = host
                        print(host)

                        ip = str(host)

                        sql_connector = mysql.connector.connect(user='python',
                                                                password='yzh8RB0Bcw1VivO3',
                                                                host='localhost',
                                                                database='Mikrotik_Hosts')

                        cursor = sql_connector.cursor()

                        add_mikrotik = ("INSERT INTO devices" "(ip)" "VALUES ('%s')" % (ip))

                        cursor.execute(add_mikrotik)
                        sql_connector.commit()
                        cursor.close()
                        sql_connector.close()


if __name__ == '__main__':
    MkScanner(host='172.31.0.0/16')


