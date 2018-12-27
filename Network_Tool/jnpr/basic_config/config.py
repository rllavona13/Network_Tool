from jnpr.junos import Device
from jnpr.junos.utils.config import Config
import json
from pprint import pprint


config_file = open('auth.json')
auth = json.load(config_file)
config_file.close()


# Para enviarle comandos al juniper usando SET commands.
def basic_config():

    try:
        dev = Device(user=auth['username'], password=auth['password'], host='10.0.1.2', port=22)
        dev.open()

        with Config(dev, mode='private') as cfg:

            cfg.load('delete interfaces fe-0/0/1 flexible-vlan-tagging ', format='set')
            cfg.pdiff()
            cfg.commit()

    except Exception as ex:
        print("Error on %s : %s" % (dev, ex))


def facts():

    try:
        dev = Device(user=auth['username'], password=auth['password'], host='10.0.1.2', port=22)
        dev.open()

        pprint(dev.facts)

    except Exception as ex:
        print("Error on %s : %s" % (dev, ex))


if __name__ == '__main__':
    basic_config()
