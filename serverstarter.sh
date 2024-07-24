#!/bin/bash
sleep 10
git --git-dir=/home/pi/earth/.git --work-tree=/home/pi/earth reset --hard HEAD
git --git-dir=/home/pi/earth/.git --work-tree=/home/pi/earth clean -n -d
git --git-dir=/home/pi/earth/.git --work-tree=/home/pi/earth pull
sleep 10

/usr/bin/node /home/pi/earth/index.js


