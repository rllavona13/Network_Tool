# this script uses Juniper NETCONF in order to backup Juniper devices configuration.
# Using Paramiko SCP module to upload the configurations files to a file server
# It can backup from any Juniper Devices specified in the JSON File

from jnpr.junos import Device
from lxml import etree
import json
import logging
import paramiko
from scp import SCPClient


config = open('config.json')
config_file = json.load(config)
config_file.close()


def config_backup():
    for host in config['hosts']:
        try:

            dev = Device(user=config['user'], password=config['pass'], host=host, port='22')
            dev.open()
            data = dev.rpc.get_config(options={'format': 'set'})
            # uncomment next line for debug purposes
            # print(etree.tostring(data)) 
            print('Creatig configuration backup for %s with  IP address:  %s' % (dev.facts['fqdn'], host))

            file_name = dev.facts['fqdn']
            f = open(file_name, 'w')
            f.write(str(etree.tostring(data)))
            f.close()

            
            local_file_path = ('/Users/rllavona/PycharmProjects/Network_Tool/Network_Tool/'
                               'jnpr/Backup_Script/' + dev.facts['fqdn'])
            remote_file_path = '/home/rrivera/backups/'

            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(hostname='10.255.6.38', username=config['username'], password=config['password'])

            scp = SCPClient(ssh.get_transport())
            print('Uploading backup files to the remote server...')
            scp.put(local_file_path, remote_file_path)
            scp.close()
            ssh.close()

        except Exception as ex:
            print("Error on %s : %s " % (host, ex))

        logging.basicConfig(filename="junos_backup_error.log", level=logging.ERROR)

if __name__ == '__main__':
    config_backup()
