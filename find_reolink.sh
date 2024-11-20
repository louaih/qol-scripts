#!/bin/bash

# Define the IP range
SUBNET="192.168.1"
START=1
END=255


echo "Scanning the network for Reolink server..."

for i in $(seq $START $END); do
    IP="$SUBNET.$i"

    # Ping each IP
    if ping -c 1 -W 1 $IP > /dev/null 2>&1; then
        echo "$IP is alive. Checking for Reolink server..."
        
        # Check for HTTP service on the specific port
        if curl -s --connect-timeout 2 "http://$IP" | grep -qi "Reolink"; then
            echo "Reolink server found at $IP"
            exit 0
        fi
    fi
done

echo "Reolink server not found on the local network."
exit 1
