#!/bin/bash

# Get the ID from the first argument
id=$1

# Format the ID to be zero-padded to two digits
formatted_id=$(printf "%02d" $id)

# Construct the IP address
ip_address="192.168.0.2${formatted_id}"

# Execute the SSH command to kill all bash processes for the user on the target machine
echo "start " $ip_address
# sshpass -p raspberrypi ssh pi@$ip_address "bash /home/pi/earth/earthstarter.sh $id"
sshpass -p raspberrypi ssh pi@$ip_address "DISPLAY=:0 nohup bash /home/pi/earth/earthstarter.sh $id > /dev/null 2>&1 &"
