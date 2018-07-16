import json
import paramiko

config_file = open('auth.json')
auth = json.load(config_file)
config_file.close()

text_backup = 'export file='
basic_backup = 'system backup save name='

client = paramiko.SSHClient()

client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(hostname='172.31.240.133', username=auth['username'], password=auth['password'])
stdin, stdout, stderr = client.exec_command(text_backup)
outlines = stdout.readlines()
output = ''.join(outlines)
print(output)


class SshConnection:
    # print("This Device: %s is a Mikrotik" % host)
    print("")
    print("Please wait... Creating %s" % Scanner.host + ".rsc Backup in the Mikrotik File System")
    print("Please wait... Creating %s" % Scanner.host + ".backup Backup in the Mikrotik File System")
    print("")
    print("Backup successfully created at the File system")
    print("")
    print("Please Wait, Gathering device information...")

    port = 22
    nbytes = 4096

    text_backup = 'export file=' + Scanner.host
    basic_backup = 'system backup save name=' + Scanner.host

    client = paramiko.Transport(host, port)
    client.connect(username=auth['username'], password=auth['password'])

    stdout_data = []
    stderr_data = []

    session = client.open_channel(kind='session')
    session.exec_command(text_backup)
    session = client.open_channel(kind='session')
    session.exec_command(basic_backup)

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
        print("")
        print("Sorry try again...")
        print("")
        client.close()