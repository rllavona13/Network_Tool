import paramiko
import json

 
config_file = open('auth.json')
auth = json.load(config_file)
config_file.close()
 
host = '172.31.240.0/24'
port = 22
nbytes = 4096
 
text_backup = 'export file=' + host
basic_backup = 'system backup save name=' + host
add_snmp_community = 'snmp community add name=publ1c read-access=yes addresses=196.12.161.0/24,192.168.253.0/24'
set_snmp_community = 'snmp set trap-community=publ1c trap-version=2'
add_radius = 'radius add address=196.12.161.54 secret=MikRadius service=login'
add_vpn_address_firewall = ' ip firewall address-list add list=Worldnet address=192.168.253.0/4'
set_use_radius = 'user aaa set use-radius=yes'

"""
Usernames and Passwords - Stored in JSON File called auth.json
"""
radius_user = auth['username']
radius_password = auth['password']
xarxa_user = auth['other_username']
xarxa_password = auth['other_password']
mik277_user = auth['mik_username']
mik277_password = auth['mik_password']

client = paramiko.Transport(host, port)
client.connect(username=radius_user, password=radius_password)

 
stdout_data = []
stderr_data = []

session = client.open_channel(kind='session')
session.exec_command(add_snmp_community)
session = client.open_channel(kind='session')
session.exec_command(set_snmp_community)
session = client.open_channel(kind='session')
session.exec_command(add_vpn_address_firewall)
session = client.open_channel(kind='session')
session.exec_command(add_radius)
session = client.open_channel(kind='session')
session.exec_command(set_use_radius)
session = client.open_channel(kind='session')
session.exec_command(text_backup)
session = client.open_channel(kind='session')
session.exec_command(basic_backup)
 
print('')
print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
print('Please wait... Configuring SNMP Community in the system...')
print('Please wait... Creating %s' % host + '.rsc Backup in the Mikrotik File System')
print('Please wait... Creating %s' % host + '.backup Backup in the Mikrotik File System')
print('')
print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
print('Backup successfully created at the File system')
print('')
print('+++++++++++++++++++++++++++++++++++++++++++++++++')
print('Please Wait, Gathering device information...')
print('')
 
while True:
    if session.recv_ready():
        stdout_data.append(session.recv(nbytes))
    if session.recv_stderr_ready():
        stderr_data.append(session.recv_stderr(nbytes))
    if session.exit_status_ready():
        break
 
session.close()
if session.recv_exit_status() == 0:
    client.close()
else:
    print('')
    print('Sorry try again...')
    print('')
client.close()