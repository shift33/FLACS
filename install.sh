#!/bin/sh
echo "This software will install new features and settings that WILL break your RaspberryPi's default setup!"
echo " "
read -r -p "Do you wish to install the FabLab System? [y/N] " response
case $response in
    [yY][eE][sS]|[yY]) 
        #Install the required packages for the system
        sudo apt-get update
        sudo apt-get install --yes --force-yes rdate
        sudo apt-get install --yes --force-yes python-mysqldb
        sudo apt-get install --yes --force-yes python-dev
        sudo apt-get install --yes --force-yes python-rpi.gpio
        sudo apt-get install --yes --force-yes python-smbus
        sudo apt-get install --yes --force-yes i2c-tools
        echo " "
        cd ~
        echo "Now altering enviornment..."
        #Add i2c support to Raspberry Pi
        sudo sed -i '$ i\i2c-dev' /etc/modules
        echo"/etc/modules [CHANGED]"
        #Comment out Blacklist File
        sudo sed -i '''s/^\([^#]\)/#\1/g' /etc/modprobe.d/raspi-blacklist.conf
        echo "/etc/modprobe.d/raspi-blacklist.conf [CHANGED]"
        #Edit rc.local to boot FabLab code on power-up
        sudo sed -i '$ i\(sudo sh /home/pi/FLACS/boot.sh)' /etc/rc.local
        echo "/etc/rc.local [CHANGED]"
        sleep 5
        #Assign existing hostname to $hostn
        hostn=$(cat /etc/hostname)
        #Display existing hostname
        echo "Existing hostname for this pi is the default $hostn"
        #Ask for new hostname $newhost
        echo "Enter new hostname: "
        read newhost
        #change hostname in /etc/hosts & /etc/hostname
        sudo sed -i "s/$hostn/$newhost/g" /etc/hosts
        sudo sed -i "s/$hostn/$newhost/g" /etc/hostname
        #display new hostname
        echo "Your new hostname is $newhost"
        echo " "
        echo "Rebooting into the FabLab Access Control System..."
        sleep 5
        sudo reboot
        ;;
    *)
        echo "Quitting..."
        ;;
esac
