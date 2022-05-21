#!/bin/bash

# run this as root!!! and rename & move to /scripts/run 
# pre req: 
# tools: tcpdump, osquery 
# dir : /reports /elf
# script : {self}

# color (optional)
RED=`tput setaf 1`
NC='\033[0m' # No Color
GREEN=`tput setaf 2`

# Directory Stuffs 
sudo rm -rf     /reports /elf 
sudo mkdir      /reports /elf 
# sudo rm /var/log/osquery/* # flush osquery logs
#mounting Host share
sudo /usr/bin/vmhgfs-fuse .host: /malware -o subtype=vmgfs-fuse,allow_other #vm mounting code!

# setting filename
share="/malware/malware"
f=$(ls $share/samples/ |  head -n 1)


printf "[+] ${GREEN}Sleeping Before Hail Marry!!!\r\n\r\n${NC}"
sleep 10 #optinal
printf "[+] ${GREEN}Executing....: $f\r\n\r\n${NC}"
printf "[+] ${GREEN}V 1.4\r\n\r\n${NC}"
printf "[+] Setting up OSQuery \r\n\r\n${NC}"
#sudo '/home/ani/scripts/osqrun' &

# dir for log collections
mkdir   $share/reports/$f 
printf "[+] ${GREEN}Directory for logger is ready!\r\n\r\n${NC}"

# copy files to VM
mv $share/samples/$f /elf 



printf "[+] ${GREEN}Sample Copied to VM: $f\r\n\r\n${NC}"
ls -lt /elf


printf "[+] ${RED} un mounting the share for safety\r\n\r\n${NC}"
sudo umount /malware

# executing hail mary
sudo chmod +x /elf/$f

# sysdig is not required. using OS Query to deal with logs
#printf "[+] ${GREEN}SYSDIG launched\r\n\r\n${NC}"
#tmux new-session -d -s sysdig 'sysdig -M 300 -w /reports/temp.scap'

printf "[+] ${GREEN}TCPDUMP launched\r\n\r\n${NC}"
tmux new-session -d -s nsm 'tcpdump -G 120 -W 1 -w /reports/temp.pcap'
sleep 1 # sleeps for 1 sec
printf "[+] ${GREEN}Executing /elf/$f\r\n${NC}"

gnome-terminal --title "Malware Infecting the system" -e /elf/$f
#./elf/$f 
sleep 1
sudo ps aux --forest >> /reports/process.txt #verify
sudo ps aux --forest | grep $f >> /reports/sample-pid.txt
printf "[+] ${GREEN}Task logger Acquired\r\n\r\n${NC}"


# EOF
# Sample Execution Wait time
printf "${RED} INFECTED VM!!!"
printf "${RED} DO not do anything here!!!"
printf "\r\n\r\n${NC}"
sleep 130

# killing
printf "[+] ${RED}Terminating Sample\r\n${NC}"
sudo pkill -f $f


# OSQuery SQL dump
sudo -u postgres pg_dump fleet > /reports/osquery.sql #DUMP DB

# Mounting and file Transfer
printf "[+] ${GREEN}  mounting the share for file transfer"
sudo /usr/bin/vmhgfs-fuse .host: /malware -o subtype=vmgfs-fuse,allow_other #vm mounting code!
ls -lh /malware                                                             #verify mount
sleep 1
mv /elf/$f $share/reports/sample_done-$f/                       # sample binary
mv /var/log/osquery/osqueryd.results.log $share/reports/$f/     # osq log export
mv /reports/* $share/reports/$f/                                # all reports
printf "[+] ${GREEN} Sample Ran successfully!\r\n${NC}"
ls -lh $share/reports/$f/


# most of the print statements are there in case of manual run and see what is happening. these will be removed in next update.