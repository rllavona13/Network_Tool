from jnpr.junos import Device
from lxml import etree
import json
import logging
import paramiko
from scp import SCPClient

# Backup en batch, IP's en el JSON.
config_file = open('config.json')
config = json.load(config_file)
config_file.close()


def config_backup():
    for host in config['hosts']:
        try:

            dev = Device(user=config['user'], password=config['pass'], host=host, port='22')
            dev.open()
            data = dev.rpc.get_config(options={'format': 'set'})
            # print(etree.tostring(data))
            print('Creando Backup de %s con IP %s' % (dev.facts['fqdn'], host))

            file_name = dev.facts['fqdn']
            f = open(file_name, 'w')
            f.write(etree.tostring(data))
            f.close()

            local_file_path = str('/home/rrivera/Backup_Script/' + dev.facts['fqdn'])
            remote_file_path = '/home/rrivera/backups/'

            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(hostname='10.255.6.38', username='rrivera', password=config['password'])

            scp = SCPClient(ssh.get_transport())
            print('Subiendo file al server...')
            scp.put(local_file_path, remote_file_path)
            scp.close()
            print('Upload Terminado')
            ssh.close()
            print('Peace OUT!')

        except Exception as ex:
            print("Error on %s : %s " % (host, ex))

        logging.basicConfig(filename="junos_backup_error.log", level=logging.ERROR)


if __name__ == '__main__':
    config_backup()