#!/bin/bash

# Get the ID from the first argument
id=$1

# Format the ID to be zero-padded to two digits
formatted_id=$(printf "%02d" $id)

# Construct the IP address
ip_address="192.168.0.2${formatted_id}"

# Check if id is zero
if [ "$id" -eq 1 ]; then
    # If id is zero, run the local ps and kill commands
    echo "Killing all bash processes for the user on the local machine"
    ps aux | grep '[e]arthstarter.sh' | awk '{print $2}' | xargs kill -9
    ps aux | grep '[e]arthcam.py' | awk '{print $2}' | xargs kill -9
else
    # Otherwise, run the SSH command to kill all bash processes for the user on the target machine
    echo "Stopping bash processes on $ip_address"
    sshpass -p raspberrypi ssh pi@$ip_address "killall -u $USER bash"
fi
