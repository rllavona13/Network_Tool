import mysql.connector
import ipaddress as ipad


iplist = open('files/framed_routes_10.csv', 'r')
for i in iplist:
    # input format: ip,route,subnet
    # example: 196.12.186.78,64.89.0.76,255.255.255.252
    # from: cat routes_email_abel.txt | awk '{print $5","$3","$4}' > framed_routes.csv
    ip, route, subnet = i.strip().split(',')
    net = str(ipad.IPv4Network(u'%s/%s' % (route,subnet),False))
    print(net)

    sql_connector = mysql.connector.connect(user='dbuser',
                                            password='dbpassword',
                                            host='196.12.161.42',
                                            database='raddb2',
                                            auth_plugin='mysql_native_password')
    cursor = sql_connector.cursor()

    query = "select username from radreply where value='%s'" % (ip)
    print(query)
    res = cursor.execute(query)

    fr ='Framed-Route'
    sql_id = 'null'
    op = ':='
    if str(res) > str(0):
        db_un = (cursor.fetchall())
        user = str(db_un)
        user_fixed = user.strip("[]()'',")
        print(user_fixed)
        query = ("insert into radreply " 
                "(`username`,`attribute`,`op`,`value`) " 
                "values ('%s','%s', '%s', '%s')" % (user_fixed, fr,op, net))
        sql_connector.commit()
        cursor.close()
        sql_connector.close()

# INSERT INTO radreply(`username`, `attribute`, `op`, `value`) VALUES('WN07000814', 'Framed-Route', ':=', '196.12.188.252/30' )
        print(query)
    else:
        print("%s doesn't exist" % ip)
