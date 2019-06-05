from jnpr.junos import Device
from lxml import etree
import json
import logging


config_file = open('config.json')
config = json.load(config_file)
config_file.close()


# Backup en batch, IP's en el JSON.
def config_backup():

    for host in config['hosts']:
        try:
            dev = Device(user=config['user'], password=config['pass'], host=host, port='22')
            dev.open()
            data = dev.rpc.get_config(options={'format': 'set'})
            # print(etree.tostring(data))
            print('Creando Backup de %s con IP %s' % (dev.facts['fqdn'], host))

            file_name = dev.facts['fqdn']
            f = open(file_name + '.txt', 'w')
            f.write(etree.tostring(data))
            f.close()

        except Exception as ex:
            print("Error on %s : %s " % (host, ex))

        logging.basicConfig(filename="junos_backup_error.log", level=logging.ERROR)


if __name__ == '__main__':
    config_backup()
