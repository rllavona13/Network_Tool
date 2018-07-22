import paramiko
import json

 
config_file = open('auth.json')
auth = json.load(config_file)
config_file.close()
 
host = '172.31.240.126'
port = 22
nbytes = 4096
 
text_backup = 'export file=' + host
basic_backup = 'system backup save name=' + host
add_snmp_community = 'snmp community add name=publ1c read-access=yes'
set_snmp_community = 'snmp set trap-community=publ1c trap-version=2'
 
client = paramiko.Transport(host, port)
 
if client.get_exception():
   
     try:
         client.connect(username=auth['other_username'], password=auth['other_password'])
 
     except:
         client.connect(username=auth['username'], password=auth['password'])
 
else:
    client.connect(username=auth['mik_username'], password=auth['mik_password'])
 
stdout_data = []
stderr_data = []
 
session = client.open_channel(kind='session')
session.exec_command(add_snmp_community)
session = client.open_channel(kind='session')
session.exec_command(set_snmp_community)
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