#!/bin/sh

sudo rdate time.nist.gov

cd /home/pi/FLACS

sudo git fetch --all

sudo git reset --hard origin/master

sudo python fablab.py
