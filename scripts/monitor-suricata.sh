#!/bin/bash

# Script for restarting suricata service via inotifywait, and systemctl. Will need sudo to run this script.
# main setup will need to activate this script on any start-up
# script: https://www.baeldung.com/linux/command-execute-file-dir-change


target = "/etc/suricata/suricata.yaml"

if [ -z "$(which inotifywait)" ]; then
    echo "inotifywait not installed. Recheck your setup.sh"
    exit 1
fi  
 
inotifywait --monitor --format "%e %w%f" --event modify,move,create,delete $target \
| while read changed; do
    echo $changed
    systemctl restart suricata.service || echo "[-] restart unsuccessful?"
done