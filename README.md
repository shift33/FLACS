FLACS
=====

###FABLab Access Control System

This project will allow a Raspberry Pi to communicate to a server to authenticate users of a machine. 
It logs visits and duration while locking out equipment to those not trained on the system.


The Raspberry Pi is the heart of the project. With its GPIO pins and embedded ARM processor, the Pi is able to become a small client located at each machine - removing the need for larger and more expensive computers. With the ability to run off of an SD Card, the Pi has the advantage of quick cloning the OS to spawn derivitive copies of itself quickly.

####To set up the first Pi, you will need the following:
	
1. SD card • Minimum size 4Gb; class 4 or higher

2. HDMI to HDMI / DVI lead • HDMI to HDMI lead OR 
		HDMI to DVI lead (for monitors with DVI input) OR
                A component video cable and TV

3. Keyboard and mouse 

4. Ethernet (network) cable OR Wireless Adapter (check if it is supported)

5. Power adapter • provide at least 700mA at 5V (wait to connect)

####Connect the components together and then follow these steps to get your Pi up and running:

1. Insert an SD card that is 4GB or greater in size into your computer
2. Format the SD card so that the Pi can read it
	* Windows
		* Download the SD Association’s Formatting Tool from
		https://www.sdcard.org/downloads/formatter_4/eula_windows/
		* Install and run the Formatting Tool on your machine
		* Set “FORMAT SIZE ADJUSTMENT” option to “ON” in the “Options” menu
		* Check that the SD card you inserted matches the one selected by the Tool
		* Click the “Format” button
	* Mac
		* Download the SD Association’s Formatting Tool from
		https://www.sdcard.org/downloads/formatter_4/eula_mac/
		* Install and run the Formatting Tool on your machine
		* Select “Overwrite Format”
		* Check that the SD card you inserted matches the one selected by the Tool
		* Click the “Format” button
	* Linux
		* We recommend using gparted (or the command line version .parted)
		* Format the entire disk as FAT
3. Download the New Out Of Box Software (NOOBS) from:
	http://downloads.raspberrypi.org/noobs
4. Unzip the downloaded file
	a. Windows - Right click on the file and choose “Extract all”
	b. Mac - Double tap on the file
	c. Linux - Run unzip [downloaded filename]
5. Copy the extracted files onto the SD card that you just formatted
6. Insert the SD card into your Pi and connect the power supply

When it boots, the the Pi will give a list of operating systems available to install. Raspbian will be selected as the default, and this is what our system is based off of.

You will then get a warning message that the SD card will be overwritten (which is fine) and then as the distribution is installed onto the SD card you will see a progress screen accompanied by helpful information about the distribution. This will take some time, so feel free to stretch your legs.

Once the file copying is complete, you will get a message “Image applied successfully”. When you hit RETURN the Raspberry Pi wil reboot, and the Raspi-Config untility will automatically run and give the following list:

* expand_rootfs			- this can be ignored, as NOOBS has done this for us.
* overscan			- this option fixes black borders around the screen if they exist.
* change_timezone		- Set this to the location of your FABLab.
* ssh 				- enable this option for later steps.
* update 			- updates the config file. Not necissary, but can be run if desired.

The Pi will finish applying the settings and may reboot. 

####Installing Libraries

We now need to install the libraries that the code will depend on. The new script allows for a seamless install of all required modules and the changes to the required files in a few easy steps.

1. At the prompt, enter the following:
```sudo git clone http://www.github.com/longblonde/FLACS```    
	This will download the entire system to the pi.
2. Once downloaded, enter the following command to start the install:
```sudo sh FLACS/install.sh```
	This command will prompt you y/n in order to proceed, as it downloads quite a few items as well as rewriting a lot of configs. THIS WILL BREAK SOME CUSTOM CONFIGURATIONS! Use at your own risk if this is not a fresh install.
3. The script will finish up by asking you for a hostname - this is one of the names of the devices set up in the database where the pi will post to.
4. Following the hostname entry, the pi will reboot into the FLACS environment and is ready for use.

####Troubleshooting
1. fablab.py is currently designed to work with an Adafruit RGB LCD Display attached. Failure to have a connected screen on boot will result in an error.
2. The system is known to not respond to the database from time to time. This is a known bug with no current fix...
