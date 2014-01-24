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
	
		Download the SD Association’s Formatting Tool from
		https://www.sdcard.org/downloads/formatter_4/eula_windows/
		ii. Install and run the Formatting Tool on your machine
		iii. Set “FORMAT SIZE ADJUSTMENT” option to “ON” in the “Options” menu
		iv. Check that the SD card you inserted matches the one selected by the Tool
		v. Click the “Format” button
	* Mac
	
		Download the SD Association’s Formatting Tool from
		https://www.sdcard.org/downloads/formatter_4/eula_mac/
		ii. Install and run the Formatting Tool on your machine
		iii. Select “Overwrite Format”
		iv. Check that the SD card you inserted matches the one selected by the Tool
		v. Click the “Format” button
	* Linux
	
		We recommend using gparted (or the command line version .parted)
		Format the entire disk as FAT
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

* expand_rootfs		- this can be ignored, as NOOBS has done this for us.
* overscan			- this option fixes black borders around the screen if they exist.
* configure_keyboard	- changes the keyboard to layout other than GB.
* change_pass			- changes password for the Pi - we will do this later.
* change_locale		- changes language options - deselect GB with spacebar.
* change_timezone		- Set this to the location of your FABLab.
* memory_split 		- can be ignored.
* ssh 				- enable this option for later steps.
* boot_behavior 		- this will be changed later, ignore for now.
* update 			- updates the config file. Not necissary, but can be run if desired.

The Pi will finish applying the settings and may reboot. When the desktop loads, be sure that your Pi is connected to the internet for the next steps.

####Installing Libraries

We now need to install the libraries that the code will depend on. Click on the desktop icon ‘LXTerminal’ to open a terminal session, and enter the following:

```sudo apt-get update```

The terminal will prompt you for a password - the default is raspberry - just press RETURN once you have entered the password. The Pi will search for updates to the system, and if it finds any it will download and install them. 

Once this finishes, we will begin by adding all of the required libraries. In the terminal, enter the following command and press y and RETURN when prompted:

```sudo apt-get install python-mysqldb```

This will install the MySQL connection service into python so that the program can communicate to our server database. After the terminal installs the above module, it will return to a blinking cursor. Then repeat the installation procedure for each of the following lines of code:

```sudo apt-get install python-dev```

```sudo apt-get install python-rpi.gpio```

These commands will install the other required dependancies of the system.
