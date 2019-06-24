from pprint import pprint
from jnpr.junos import Device
import json


config_file = open('configuration.json')
config = json.load(config_file)
config_file.close()


def facts():
    try:
        for host in config['hosts']:
            dev = Device(user=config['user'], password=config['pass'], host=host, port='22')
            dev.open()
            pprint(dev.facts)
            dev.close()

    except Exception as ex:
        print("Error on %s : %s " % (host, ex))


if __name__ == '__main__':

    facts()
    print("")
    print("Script By Ramon Rivera Llavona")
    print("")
 