from jnpr.junos import Device
from jnpr.junos.utils import config
from pprint import pprint
import json


config_file = open('configuration.json')
auth = json.load(config_file)
auth.close()

for host in config['hosts']:
    try:
        dev = Device(user=auth['user'], password=auth['pass'], host=host, port='22')
        dev.open()

    except Exception as ex:
        print("Error on %s : %s " % (host, ex))
