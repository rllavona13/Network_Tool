#!/usr/bin/python3.7

import mysql.connector
import ipaddress as ipad
import getpass

"""
diffpass = True
while diffpass:
    dbpass = getpass.getpass("Enter database password for user rrivera: ")
    dbpass2 = getpass.getpass("Confirm password: ")
    if dbpass == dbpass2:
        diffpass = False
        
    else:
        print("ERROR: Password mismatch")


    
#db = mysql.connect(host='', user='rrivera', passwd=dbpass, db='raddb2')
#cur = db.cursor()
"""

iplist = open('framed_routes_10.csv', 'r')
for i in iplist:
    # input format: ip,route,subnet
    # example: 196.12.186.78,64.89.0.76,255.255.255.252
    # from: cat routes_email_abel.txt | awk '{print $5","$3","$4}' > framed_routes.csv
    (ip, route, subnet) = i.strip().split(',')
    net = str(ipad.IPv4Network(u'%s/%s' % (route, subnet), False))
    print(net)
    sql_connector = mysql.connector.connect(user='rrivera',
                                            password='R4ym0nd12@',
                                            host='196.12.161.42',
                                            database='raddb2',
                                            auth_plugin='mysql_native_password')
    cursor = sql_connector.cursor()

    query = "select username from radreply where value='%s'" % ip
    res = cursor.execute(query)


    if res > 0:
        db_un = cursor.fetchall()
        query = "insert into radreply (`username`,`attribute`,`op`,`value`) values ('%s','Framed-Route',':=','%s')" % \
                (db_un, net)
    else:
        print("%s doesn't exist" % ip)
