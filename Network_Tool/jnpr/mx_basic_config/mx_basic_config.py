from jnpr.junos import Device
from jnpr.junos.utils.config import Config
import json


config_file = open('config.json')
config = json.load(config_file)
config_file.close()


def mx_basic_config():
    try:
        for host in config['hosts']:
            dev = Device(user=config['user'], password=config['pass'], host=host, port='22')
            dev.open()
            with Config(dev.open(), mode='private') as cu:
                #cu.load('set system services netconf traceoptions file test.log', format='set')
                cu.load(path='config.xml', format='set', merge=True)
                cu.pdiff()
                cu.commit()
            dev.close()

    except Exception as ex:
        print ("Error on %s : %s " % (host, ex))


if __name__ == '__main__':
    mx_basic_config()
