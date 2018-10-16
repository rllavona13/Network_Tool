import napalm
from napalm_ros import ros
import getpass

router = '172.30.247.181'
router_port = '8729'
user = 'rrivera'
password = getpass.getpass

driver = napalm.get_network_driver('ros')

print('Connecting to', router, "on port", router_port, "as", user)

device = driver(hostname=router, username=user,
                password=password, optional_args={'port': router_port})

print('Opening ...')
device.open()