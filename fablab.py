#!/usr/bin/env python
#*- coding: utf-8 -*-
#
# v0.3.0 FLACS
# Dan Wald

import MySQLdb as mdb
import sys
import socket
from time import strftime
from time import sleep
from Adafruit_CharLCDPlate import Adafruit_CharLCDPlate
try:
    import RPi.GPIO as GPIO
except RunTimeError:
    print ("Must run as ROOT! - Try using SUDO!")

#Database variables
host = "192.168.1.145"
password = "password"
database = "FabControl"

#Set up the LCD object, clear the screen, and display program version
lcd = Adafruit_CharLCDPlate()
lcd.clear()
lcd.message("FABLab Login\nSystem v1.0")
col = (lcd.RED, lcd.GREEN, lcd.BLUE, lcd.ON)
for c in col:
    lcd.backlight(c)
    sleep(1)
lcd.clear()
lcd.message("Connecting to\nDatabase...")
lcd.backlight(lcd.YELLOW)

#These variables control the Database connection
#The User is set via the hostname of the Pi itself
#To change the hostname:
#edit both /etc/hosts and /etc/hostname to the new name
#To take effect, reboot the system
#Connect to database:
user = socket.gethostname()
db=mdb.connect(host,user,password,database);
#Create connection object:
c = db.cursor()

#The following sets the GPIO assignments for the relay
GPIO.setwarnings(False)   #Sets warnings off to reduce clutter
GPIO.setmode(GPIO.BOARD)  #Sets GPIO numbering to 1-26
GPIO.setup(12, GPIO.OUT)  #Sets Pin 12 (BCM 18) to output
GPIO.output(12, GPIO.LOW) #Sets default state to off

#The following values do not matter to this program,
#however, are relevant to the Windows Admin CMS
#DO NOT MODIFY:
id = 0 
organisation = 0
facility = 0
location = socket.gethostname() #Sets device hostname as location
hostname = socket.gethostname() #Sets device hostname as hostname
terminal = 0
software = 20011
operator = 0

#Set up Scan Code for Program:
def scan():
    while (True):
        try:
            lcd.clear()
            lcd.backlight(lcd.BLUE)
            lcd.message("SCAN BARCODE:")
            x = int(raw_input("SCAN BARCODE: "))
            
        except ValueError:
            print "Not A Valid User! Must be number in format XXXXXX."
            print ""
            lcd.clear()
            lcd.backlight(lcd.RED)
            lcd.message("User does\nNOT exist!")
            sleep(5)
            continue
        else:
            return (x)

#Set up timestamp for visit logs
logtime = strftime("%Y-%m-%d %H:%M:%S")

#Return database version:
c.execute("SELECT VERSION()")
ver=c.fetchone()
print "DB Version: %s" % ver
lcd.clear()
lcd.message("%s" %ver)

#Begin program loop
while (True):
    print ""
    barcode=scan()
    lcd.backlight(lcd.GREEN)
    lcd.message("\nScanned")
    sleep(.5)
    
    #Start FabLab Status Check:
    c.execute("""SELECT status FROM fabstatus WHERE machine = %s""", ("fablab"))
    labstatus = c.fetchone()
    if labstatus[0] == 1:
        print "Fablab is Open"
        lcd.clear()
        lcd.backlight(lcd.GREEN)
        lcd.message("FABLab is OPEN")
        sleep(.5)

        #Start Machine Status Check:
        c.execute("""SELECT * FROM fabstatus WHERE machine = %s""", (hostname))
        machineresult = c.fetchone()
        machinestatus = machineresult[3]
        binid = machineresult[1]
        if machinestatus == 1:
            print "%s is available" %hostname
            lcd.backlight(lcd.GREEN)
            lcd.message("\n%s is OPEN" %hostname)
            sleep(.5)

            #Start User Status Check:
            c.execute("""SELECT objid FROM scancode WHERE code = %s""",(barcode))
            objid = c.fetchone()
            print "UserID: ", objid[0]
            if objid is not None:
                c.execute("""SELECT name, surname, flags FROM contact WHERE id = %s""",objid[0])
                fabuser = c.fetchone()
                print fabuser
                name = fabuser[0] + " " + fabuser[1]
                print name
                access = fabuser[2] & binid
                print "Flag: ", access                
                if access > 0:
                    
                    #Grant or Deny Access:
                    try:
                        logBit = 1
                        facility = 1
                        #Log the time of the barcode scan:
                        c.execute(("""INSERT INTO visitlog (id, member, logtime, logcode, \
                        organisation, facility, location, hostname, terminal, software, operator) \
                        values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""),\
                        (id, fabuser[2], logtime, logBit, organisation, facility, location, hostname, terminal, software, operator))
                        db.commit()

                        #This line sets the machine as IN USE by the current user:
                        c.execute("""UPDATE fabstatus SET status = 2, contactid = %s, name = %s WHERE machine = %s""", (objid[0], name, hostname))                                  
                        db.commit()

                        #Lastly, turn on the relay
                        GPIO.output(12, GPIO.HIGH)
                        print "Logged SUCCESS to database"
                        lcd.clear()
                        lcd.backlight(lcd.GREEN)
                        lcd.message("CURRENT USER:\n%s" % (name))
                        sleep(.5)

                        #Wait for user to log out
                        raw_input("PRESS ENTER TO LOG OUT ->")

                        #Reset log status to log-out
                        logBit = 0
                        facility = 1
                        c.execute(("""INSERT INTO visitlog (id, member, logtime, logcode, \
                        organisation, facility, location, hostname, terminal, software, operator) \
                        values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""),\
                        (id, fabuser[2], logtime, logBit, organisation, facility, location, hostname, terminal, software, operator))
                        db.commit()

                        #Resets the machine to available by the current user:
                        c.execute("""UPDATE fabstatus SET status = 1, contactid = 0, name = '' WHERE machine = %s""", (hostname))                                  
                        db.commit()

                        #Lastly, turn off the relay
                        GPIO.output(12, GPIO.LOW)
                        print "Logged out of database"
                                            
                    except mdb.ProgrammingError:
                        print "DATABASE ERROR!"
                        pass
                        db.rollback()
                        
                #User access level failure
                else:
                    print "Access Denied! Please See a Lab Tech"
                    lcd.clear()
                    lcd.backlight(lcd.RED)
                    lcd.message("Access Denied!\nSee a Lab Tech")                    
                    #Log scan without triggering GPIO - set 
                    logBit = 0
                    facility = 0
                    c.execute(("""INSERT INTO visitlog (id, member, logtime, logcode, \
                    organisation, facility, location, hostname, terminal, software, operator) \
                    values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""),\
                    (id, fabuser[2], logtime, logBit, organisation, facility, location, hostname, terminal, software, operator))
                    db.commit()
                    sleep(5)
                    
            #User exist level failure
            else:
                print "User does not exist!"
                lcd.clear()
                lcd.backlight(lcd.RED)
                lcd.message("User does\nNOT exist!")
                sleep(5)
            
        #Machine access level - use codes to set status:                
        elif machinestatus == 2:
            print "%s is IN USE" %hostname
            lcd.clear()
            lcd.backlight(lcd.RED)
            lcd.message("%s\nis in use" % (hostname))
            sleep(5)
            
        elif machinestatus == 3:
            print "%s is under repair" %hostname
            lcd.clear()
            lcd.backlight(lcd.RED)
            lcd.message("%s\nis under repair" % (hostname))
            sleep(5)
            
        else:
            print "%s is offline" %hostname
            lcd.clear()
            lcd.backlight(lcd.RED)
            lcd.message("%s\nis offline" % (hostname))
            sleep(5)
            
    #Lab access level    
    else:
        print "FabLab is closed"
        lcd.clear()
        lcd.backlight(lcd.RED)
        lcd.message("FABLab is closed")
        sleep(5)

    
    

    
    





