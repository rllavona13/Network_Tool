from jnpr.junos import Device
from lxml import etree
import json


config_file = open('humacao.json')
config = json.load(config_file)
config_file.close()


# Backup en batch, IP's en el JSON.
def config_backup():

    for host in config['hosts']:
        try:
            dev = Device(user=config['user'],
                         password=config['pass'],
                         host=host, port='22')
            dev.open()
            data = dev.rpc.get_config(options={'format': 'set'})
            print(etree.tostring(data))

            file_name = dev.facts['fqdn']
            f = open(file_name + '.txt', 'w')
            f.write(etree.tostring(data))
            f.close()

        except Exception as ex:
            print("Error on %s : %s " % (host, ex))


# Backup sin loop, solo 1 device
def backup():

    dev = Device(user=config['user'], password=config['pass'], host='10.1.1.2', port='22')
    dev.open()
    data = dev.rpc.get_config(options={'format': 'set'})
    print(etree.tostring(data))
    file_name = dev.facts['fqdn']
    f = open(file_name + '.txt', 'w')
    f.write(etree.tostring(data))
    f.close()


if __name__ == '__main__':
    config_backup()
