# Abstract 

We propose a novel sandbox for analyzing Linux malware. Our sandbox system, called Vajra-sand, supports dynamic analysis for elf binaries and has some features to automate and facilitate malware analysis. In addition, our system collects packet capture files using tcpdump for network granular logs. With the dataset of real-world malware, we proved that our sandbox system can analyze Linux malware which is specifically designed for infecting Linux systems. Through an analysis experiment on many malware samples, we show a possibility that our system could facilitate a large-scale analysis in an automated manner and retrieve further insights from Linux malware. 

# Working of Varjra Sandbox 

Varja Sandbox requires a proper file system on Host & VM to work properly and some pre-configured settings.  

File Structure HOST 

|direcotry| decription|
|---|---|
|`C:\malware\` |[root directory] |
|`C:\malware\done_sample` |[store sample after successful execution   |
|`C:\malware\reports` 	|[store reports of all executed samples]    |
|`C:\malware\samples	`    |[sample to be executed inside our sandbox] | 

File Structure inside Sanbox VM  
|direcotry| decription|
|---|---|
|`/ 		`    |[root directory] |
|`/scripts`	|[our bash script to automate the log collections] |
|`/elf `		|[sample drop in this location by our automation script] |
|`/reports`	|[temp reports generated in this location before pulling out to host machine]| 


## Execution process 

|HOST/VM| Process|
|---|---|
|HOST: `vm_automation.py`|VM starts with a saved snapshot |
|HOST: `vm_automation.py`|Automated script triggers SSH command to execute our logger script inside VM |
|Sandbox: run|Logger script mounts host system and copy malware sample inside VM and unmount share |
|Sandbox: run|Logger executes tcpdump  & clears any artifacts from OSQuery logs  |
|Sandbox: run|Logger executed malware and waited for 120 sec. Created a PID file for sanity check |
|Sandbox: run|Logger kill malware process id  |
|Sandbox: run|Logger mounted back the network share send all reports (tcpdump, osquery logs & PID |checks) to host directory c:\malware\reports\{sample_name} 
|Sandbox: run|Logger sent a notification in telegram |
|HOST: `vm_automation.py`|HOST automation now ready to kill the VM and move the executed samples to |C:\malware\done_sample\{sample_name} 
|HOST: `vm_automation.py`|HOST automation look for any other available binary in c:\malware\samples location if there is more repeat the same process, else shut down VM and exit out. |
 

# Dynamic Analysis Features (OSquery logs)

* Filtered call trace for tracing system calls related to file, process, network activity 
* Unfiltered call trace - traces all system calls (noisier)  
* Filtered system event monitoring to track file, process, network activity (less noisy)  
* Unfiltered system even monitoring to track file, process, network, memory allocations/unallocations, signals etc. (noisier)  
* Shows DNS summary  
* Shows TCP conversations  
* Stores packet captures  
* Stores event trace dump 
* Execution process 

---

This project is hosted by #IITB