#!/usr/bin/python3.7
import MySQLdb
import ipaddress as ipad
import getpass

diffpass = True
while diffpass:
    dbpass = getpass.getpass("Enter database password for user rrivera: ")
    dbpass2 = getpass.getpass("Confirm password: ")
    if dbpass == dbpass2:
        diffpass = False
    else:
        print("ERROR: Password mismatch")

db = MySQLdb.connect(host='196.12.161.42', user='rrivera', passwd=dbpass, db='raddb2')
cur = db.cursor()

iplist = open('framed_routes_10.csv', 'r')
for i in iplist:
    # input format: ip,route,subnet
    # example: 196.12.186.78,64.89.0.76,255.255.255.252
    # from: cat routes_email_abel.txt | awk '{print $5","$3","$4}' > framed_routes.csv
    ip, route, subnet = i.strip().split(',')
    net = str(ipad.IPv4Network(u'%s/%s' % (route, subnet), False))
    query = "select username from radreply where value='%s'" % ip
    res = cur.execute(query)
    if res > 0:
        db_un = cur.fetchall()[0][0]
        query = "insert into radreply (`username`,`attribute`,`op`,`value`) values ('%s','Framed-Route',':=','%s')" % \
                (db_un, net)
        print(query)
    else:
        print("%s doesn't exist" % ip)
