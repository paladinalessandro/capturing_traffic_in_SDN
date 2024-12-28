#!/bin/bash

# Ensure script runs with root privileges
if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root" 
   exit 1
fi

# Loop to perform 5 captures
for i in $(seq 1 5); do
    echo "Starting capture $i..."
    sudo timeout 6 tcpdump -w "malicious$i.pcap"
    echo "Capture $i completed and saved as malicious$i.pcap"
done

echo "All 5 malign captures completed."
