from napalm_ros import ros
import napalm
import napalm_ros


router_ip = '192.168.1.1'
router_port = 8728 # Use 8729 for api-ssl
router_user = 'rrivera'
router_pass = 'R4ym0nd12@'

driver = napalm.get_network_driver('ROS')

print('Connecting to', router_ip, "on port", router_port, "as", router_user)

device = driver(hostname=router_ip, username=router_user,
                password=router_pass, optional_args={'port': router_port})

print('Opening ...')
device.open()