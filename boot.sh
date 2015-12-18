#!/bin/sh

sudo rdate time.nist.gov

cd /home/pi/FLACS


#These lines pull updates from the git repo - uncomment to pull newest code on boot.
#sudo git fetch --all

#sudo git reset --hard origin/master

sudo python fablab.py
