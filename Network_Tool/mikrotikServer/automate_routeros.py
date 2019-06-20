import napalm
from pprint import pprint
import json

router_ip = '196.12.180.5'

auth_file = open('auth.json')
login = json.load(auth_file)
auth_file.close()

driver = napalm.get_network_driver('ROS')

host = router_ip
user = login['username']
password = login['password']

def mik_con(host, user, password, port=8729):


    device = driver(hostname=host, username=user,
                    password=password, optional_args={'port': port})
    print('Opening ...')
    device.open()
    print('Connecting to', host, "on port", port, "as", user)
    print('')

    ipAddress = str(device.get_interfaces_ip()['vlan0024']['ipv4'])
    ipAddressFix = (ipAddress.strip("{ ' } ' : ': {'prefix_length': 30"))

    print(ipAddressFix)

    device.close()


mik_con(host=router_ip, user=login['username'], password=login['password'])