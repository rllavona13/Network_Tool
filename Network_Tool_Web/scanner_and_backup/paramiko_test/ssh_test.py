import paramiko
import json
from pysnmp.entity.rfc3413.oneliner import cmdgen

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


class GetIdentity:

    def __init__(self):
        pass

    # host = '172.31.240.133'

    snmp_gen = cmdgen.CommandGenerator()

    mikrotik_identity = 'iso.3.6.1.2.1.1.5.0'

    values = errorindication, errorstatus, errorindex, varbinds = snmp_gen.getCmd(
        cmdgen.CommunityData('publ1c'),
        cmdgen.UdpTransportTarget(((host), 161)), mikrotik_identity)

    for name, val in varbinds:
        device_name = val


class GetVersion:

    def __init__(self):
        pass

    # host = '172.31.240.133'

    snmp_gen = cmdgen.CommandGenerator()

    mikrotik_version = 'iso.3.6.1.2.1.47.1.1.1.1.2.65536'

    values = errorindication, errorstatus, errorindex, varbinds = snmp_gen.getCmd(
        cmdgen.CommunityData('publ1c'),
        cmdgen.UdpTransportTarget(((host), 161)), mikrotik_version)

    for name, val in varbinds:
        device_version = val


class GetModel:

    def __init__(self):
        pass

    # host = '172.31.240.133'

    snmp_gen = cmdgen.CommandGenerator()

    mikrotik_model = 'iso.3.6.1.2.1.1.1.0'

    values = errorindication, errorstatus, errorindex, varbinds = snmp_gen.getCmd(
        cmdgen.CommunityData('publ1c'),
        cmdgen.UdpTransportTarget(((host), 161)), mikrotik_model)

    for name, val in varbinds:
        device_model = val


identity = str(GetIdentity.device_name)
version = str(GetVersion.device_version)
model = str(GetModel.device_model)
ip = str(host)

print('DEVICE INFO:')
print('IP Address: ' + host)
print('Name: ' + identity)
print('RouterOS Version: ' + version)
print('Mikrotik Model: ' + model)
print('By: Ramon Rivera - Neo Data')
print('+++++++++++++++++++++++++++++++++++++++++++++++++')