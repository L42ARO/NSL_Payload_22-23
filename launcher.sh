#!/bin/sh
# launcher.sh
# navigate to home directory, then to this directory, then execute python script, then back home
#cd ~/NSL_22-23/NSL_Payload_22-23/ZERO-DEV
#pigpiod
cd /home/rocketman/NSL_22-23/NSL_Payload_22-23/ZERO-DEV
pwd
python my_zero.py
cd /
