#!/bin/bash

# Ensure script runs with root privileges
if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root" 
   exit 1
fi

# Loop to perform 20 captures
for i in $(seq 1 20); do
    echo "Starting capture $i..."
    sudo timeout 6 tcpdump -w "$i.pcap"
    echo "Capture $i completed and saved as $i.pcap"
done

echo "All 20 captures completed."
