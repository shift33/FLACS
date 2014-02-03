#!/bin/sh

sudo apt-get update

sudo apt-get install --yes --force-yes python-mysqldb

sudo apt-get install --yes --force-yes python-dev

sudo apt-get install --yes --force-yes python-rpi.gpio

sudo apt-get install --yes --force-yes python-smbus

sudo apt-get install --yes --force-yes i2c-tools

sudo nano /etc/modules

sudo nano /etc/modprobe.d/raspi-blacklist.conf

sudo nano /etc/rc.local

