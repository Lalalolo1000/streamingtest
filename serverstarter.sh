#!/bin/bash
sleep 10
git --git-dir=/home/pi/earth/.git pull
sleep 10

/usr/bin/node /home/pi/earth/index.js

reboot


