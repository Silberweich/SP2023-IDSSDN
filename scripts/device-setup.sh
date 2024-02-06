#!/bin/bash
# script for setting up a system both controller and IDS/SW. will need sudo to run.
# res: https://unix.stackexchange.com/questions/3886/difference-between-nohup-disown-and
# disown a process, surimon.sh
# res: https://docs.suricata.io/en/suricata-6.0.0/rule-management/suricata-update.html
# suricata-update utilities

# functions

setup-monitor-suricata (){
    # firstly,add
    # lastly 
    disown ./monitor-suricata.sh
    # or something of sort
}

# main
apt update || echo "[-] apt update failed" && exit
apt upgrade -y || echo "[-] apt upgrade failed" && exit

if [ -z "$(which inotifywait)" ]; then
    echo "[+] inotifywait not installed. Installing..."

    apt install inotify-tools
fi

if [ -z "$(which python)" ]; then
    echo "[+] python not installed. Installing..."

    apt install python
fi

if [ -z "$(which crontab)" ]; then
    echo "[+] cronjob not installed. Installing..."

    apt install cronie
fi

if [ -z "$(which ryu-manager)" ]; then
    echo "[+] installing ryu-controller via pip"

    pip install ryu
fi

if [ -z "$(which suricata-update)" ]; then
    echo "[+] suricata not installed. Installing..."

    add-apt-repository ppa:oisf/suricata-stable
    apt install suricata
    systemctl enable suricata.service
    suricata-update
fi

if [ -z "$(which ovs-vsctl)"]; then 
    echo "[+] ovs not installed. Installing..."

    apt install openvswitch-switch
    apt install openvswitch-common
    systemctl enable openvswitch-switch.service
fi

# utility
if [ -z "$(which nmap)" ]; then
    echo "[+] installing nmap, for network utility"
    apt install nmap
fi