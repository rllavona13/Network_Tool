import napalm
from pprint import pprint
import json
import netmiko
import librouteros
import ssl
from librouteros.login import login_plain, login_token


method = (login_plain)
router_ip = '196.12.180.5'

auth_file = open('auth.json')
login = json.load(auth_file)
auth_file.close()

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

#driver = napalm.get_network_driver('ROS')
host = router_ip
user = login['username']
password = login['password']


ros = librouteros.connect(host=router_ip, username=user, password=password)


print(ros)


"""

def mik_con(host, user, password, port=8729):


    device = driver(hostname=host, username=user,
                    password=password, optional_args={'port': port})
    print('Opening ...')
    device.open()
    print('Connecting to', host, "on port", port, "as", user)
    print('')

    #ipAddress = str(device.get_interfaces_ip()['vlan0024']['ipv4'])
    #ipAddressFix = (ipAddress.strip("{ ' } ' : ': {'prefix_length': 30"))
    mk_config = device.get_config(retrieve=u'all')

    print(mk_config)

    #print(ipAddressFix)

    device.close()



mik_con(host=router_ip, user=login['username'], password=login['password'])
"""