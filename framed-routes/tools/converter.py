import ipaddress as ipad

iplist = open('framed_routes_10.csv', 'r')
for i in iplist:
    # input format: ip,route,subnet
    # example: 196.12.186.78,64.89.0.76,255.255.255.252
    # from: cat routes_email_abel.txt | awk '{print $5","$3","$4}' > framed_routes.csv
    (ip, route, subnet) = i.strip().split(',')
    net = (ipad.IPv4Network(u'%s/%s' % (route, subnet), False))
    print(f'{net}')
    #print(net)