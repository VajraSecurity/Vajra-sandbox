import os
import time
from os import listdir
from os.path import isfile, join
import paramiko # SSH lib


## VM config 
# ======================================== #
host = "VM_IP"
username = "VM_USERNAME"
password = "VM_PASSWORD"
vmrun_path = "vmrun.exe" 
command = "sudo bash /scripts/run | tee ~/reports/run.log" #Exec /scripts/run inside VM; run script is inside vm_scripts folder

log_path = "C:\\Users\\anime\\Desktop\\Malware\\reports"    #log paths
done_sample="C:\\Users\\anime\\Desktop\\Malware\\"          # Samples after execution will be moved here
snapshot_name = '"wishssh"' #withSSH 

# Fancy Countdown timer; not required anymore but here for debug env. 
def countdown(t):
    while t:
        mins, secs = divmod(t, 60)
        timer = '{:02d}:{:02d}'.format(mins, secs)
        print(timer, end="\r")
        time.sleep(1)
        t -= 1
    print('File Ran Sucessfully!!')
# input time in seconds
t = 1

start_command = f'{vmrun_path} -T ws -gu {username} -gp {password} '
vm_path = '"D:\\vms\\Ubuntu-Prod\\Ubuntu-Prod.vmx"'         # VM path

# malware stuffs
all_dir = 'C:\\Users\\anime\\Desktop\\Malware\\samples'     # Malware Sample location

onlyfiles = [f for f in listdir(all_dir) if isfile(join(all_dir, f))]

if not onlyfiles:
    print ("Nothing to do here")
    print ("put some malware at: " + all_dir) 
    print("============={Mission Failed Sucessfully}=============")
else: 
    print('got something to execute....')
    ## VM exection 
    # ======================================== #

    for f in onlyfiles:

        # reverting to Snap 
        print("Reverting Snapshot!")                        # Snapshot of VM with OSQ running & configured properly. 
        os.system(f'{start_command} revertToSnapshot {vm_path} {snapshot_name}')
        time.sleep(5)
        #powering ON 
        print("Starting VM!")
        os.system(f'{start_command} start {vm_path}')
        #Execution `run.sh`
        print("SSH into VM & Executing run.sh!")
        client = paramiko.client.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(host, username=username, password=password)
        _stdin, _stdout,_stderr = client.exec_command(command)
        print(_stdout.read().decode())
        client.close()
        print("VM Execution Done!")
        # WAIT for the sample execution  
        countdown(int(t))
        print("Copying Logs!")
        time.sleep(1)
        print("Sample Log Collection Done sucessfully")
        print("VM Stopping!")
        os.system(f'{start_command} stop {vm_path}')
        os.system(f'move "{join(all_dir, f)}" "{join(done_sample, "done_sample/", f)}"')