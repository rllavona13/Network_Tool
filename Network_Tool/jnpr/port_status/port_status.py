from jnpr.junos import Device
from jnpr.junos.op import phyport
import json


config_file = open('configuration.json')
config = json.load(config_file)
config_file.close()


def port_status():

    for host in config['hosts']:
        try:
            dev = Device(user=config['user'], password=config['pass'], host=host, port='2')
            dev.open()
            ports = phyport.PhyPortTable(dev).get()
            print('-' * 65)
            print("Host: %s" % host)
            print("%s%s%s" % ("Interface".ljust(12), "Status".ljust(8), "Time Since Last Flap".ljust(45)))
            print('-' * 65)
            print
            for port in ports:
                print("%s%s%s" % (port.name.ljust(12), port.oper.ljust(8), port.flapped.ljust(45)))

        except Exception as ex:
            print("Error on %s : %s " % (host, ex))


if __name__ == '__main__':
    port_status()
    print("")
    print("")
    print("Script By Ramon Rivera")
