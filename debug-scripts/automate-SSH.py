import paramiko

command = "sudo whoami >> /home/ani/Desktop/id.log"

# Update the next three lines with your
# server's information

host = "192.168.216.130"
username = "ani"
password = "admin"

client = paramiko.client.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(host, username=username, password=password)
_stdin, _stdout,_stderr = client.exec_command(command)
print(_stdout.read().decode())
client.close()