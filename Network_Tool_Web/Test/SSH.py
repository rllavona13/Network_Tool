import paramiko
import json

config_file = open('auth.json')
config = json.load(config_file)
config_file.close()

ip = '172.31.240.133'

mk_lst = []
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(hostname=ip, username=config['username'], password=config['password'])
ssh.invoke_shell()
stdin, stdout, stderr = ssh.exec_command('system identity print\n' 'system routerboard print\n' 'ip address print')
print(stdout.read())
mk_lst.append(stdout.read())
print(mk_lst)
ssh.close()
