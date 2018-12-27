from jnpr.junos import Device
from jnpr.junos.utils import config
from pprint import pprint
import json


config_file = open('configuration.json')
config = json.load(config_file)
config_file.close()

for host in config['hosts']:
    try:
        dev = Device(user=config['user'], password=config['pass'], host=host, port='22')
        dev.open()

    except Exception as ex:
        print "Error on %s : %s " % (host, ex)
