#!/bin/bash

sleep 10

for ((n=0;n<3;n++))
do
 wget -O earthcam.py 192.168.0.201:8000/earth/$1
 python3 earthcam.py
 git --git-dir=/home/pi/earth/.git pull
 sleep 10
done
