# This script is for configure Juniper Ports using Juniper NETCONF

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
        
def send_cmd():
    
    client1 = paramiko.SSHClient()
    client1.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client1.connect(IP, username=username, password=password)
    configure = client1.invoke_shell()
    configure.send('configure')
    configure.send('set interfaces ge-0/0/10 description "test"')
    configure.send('show | compare')
    configure.recv(1000)

    client1.close()


if __name__ == '__main__':

    facts()
    print("")
    print("Script By Ramon Rivera Llavona")
    print("")
 
