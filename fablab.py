#!/usr/bin/env python
#*- coding: utf-8 -*-

"""fablab.py accesses the central control database to verify users against the lab machines"""

__author__ = "Dan Wald"
__copyright__ = "Copyright 2015, UWStout FABLab"
__credits__ = ["Dan Wald", "Sam Armstrong", "Lady Ada & Adafruit"]
__license__ = "GPL"
__version__ = "0.6" #No major changes from 5.51, just noting final supported version before abandonment.
__maintainer__ = "Dan Wald"
__email__ = "waldd@my.uwstout.edu"
__status__ = "Prototype - Finished"

import MySQLdb as mdb
import os
import sys
import socket
import time
import datetime
from time import strftime
from time import sleep
from Adafruit_CharLCDPlate import Adafruit_CharLCDPlate
try:
    import RPi.GPIO as GPIO
except RunTimeError:
    print ("Must run as ROOT! - Try using SUDO!")

host = "192.168.2.12"                                                    #Database host
user = socket.gethostname()                                             #Database user - see note 1
password = "FabContro1" 	                                            #Database password
database = "fabcontrol"                                                 #Database tables

techflag = 1                                                            #Tech Flag for admin bypass


GPIO.setwarnings(False)                                                 #Sets warnings off to reduce clutter
GPIO.setmode(GPIO.BOARD)                                                #Sets GPIO numbering to 1-26
GPIO.setup(12, GPIO.OUT)                                                #Sets Pin 12 (BCM 18) to output
GPIO.output(12, GPIO.LOW)                                               #Sets default state to off

id = 0                                                                  #These variables satisfy the admin cms
organisation = 0                                                        
facility = 0                                                            #Will be manipulated later for logging
location = socket.gethostname()                                         #Sets device hostname as location
hostname = socket.gethostname()                                         #Sets device hostname as hostname
terminal = 0                                                            
software = 20011                                                        
operator = 0                                                            

lcd = Adafruit_CharLCDPlate() #Use Adafruit library for i2c and screen
vers = __version__ #Sets version number for screen

def scan(): #Set up Scan Code for Program
    while (True):
        try:
            lcd.clear()
            lcd.backlight(lcd.BLUE)
            lcd.message("SCAN BARCODE:")
            x = int(raw_input("SCAN BARCODE: "))
            
        except ValueError: #Input format error handling
            lcd.clear()
            lcd.backlight(lcd.RED)
            lcd.message("User does\nNOT exist!")
            print "User does NOT exist!"
            print ""
            sleep(5)
            continue
        else:
            return (x)

lcd.clear() #Clear LCD
lcd.message("FABLab Login\n%s" % (vers)) #Display program version
col = (lcd.RED, lcd.GREEN, lcd.BLUE, lcd.ON) #Cycle FABLab colors
for c in col:
    lcd.backlight(c)
    sleep(1)


lcd.clear()
lcd.backlight(lcd.YELLOW) #Sets LCD Warning mode
lcd.message("Connecting")
sleep(.25)
lcd.clear()
lcd.message("Connecting.")
sleep(.25)
lcd.clear()
lcd.message("Connecting..")
sleep(.25)
lcd.clear()
lcd.message("Connecting...")
db=mdb.connect(host,user,password,database); #Tries connection to database
c = db.cursor() #Creates cursor object if successful

    
#Return database version:
c.execute("""SELECT VERSION()""")
ver = c.fetchone()
lcd.clear()
lcd.backlight(lcd.ON)
lcd.message("%s" %ver)
print "%s" % (ver)



#Find Machine Flag for Binid
c.execute("""SELECT id FROM contactflag WHERE vtext = %s""", (hostname))
machineresult = c.fetchone()
binid = 2**machineresult[0]
print "binid: ",binid
lcd.message("\n%s" %binid)
sleep(2)

c.close()

#Begin program loop
while (True):
    print ""
    barcode=scan()
    
    if (barcode == 000000): #START CHECK FOR SHUTDOWN CODE
        lcd.clear()
        lcd.message("SHUTDOWN STARTED")
        col = (lcd.RED, lcd.YELLOW, lcd.RED, lcd.YELLOW, lcd.RED, lcd.YELLOW, lcd.RED)
        for c in col:
            lcd.backlight(c)
            sleep(.25)
        os.system("sudo shutdown -h now")
        break
        
    lcd.backlight(lcd.GREEN)
    lcd.message("\nScanned")
    sleep(.5)
    
#New server connection Scheme - could be problimatic:
#----------------------------------------------------
    try:
        lcd.clear()
        lcd.backlight(lcd.YELLOW) #Sets LCD Warning mode
        lcd.message("Accessing FABLab")
        sleep(.2)
        db=mdb.connect(host,user,password,database); #Tries connection to database
        c = db.cursor() #Creates cursor object if successful
        
    except mdb.Error, e: #DB connection error handling
        lcd.clear()
        lcd.backlight(lcd.VIOLET)
        lcd.message("SERVER NOT FOUND\nRESTART SCANNER")
        break    
#----------------------------------------------------
    
    #Start User Status Check:
    c.execute("""SELECT objid FROM scancode WHERE code = %s""",(barcode))
    objid = c.fetchone()
    if objid is not None:
        c.execute("""SELECT name, surname, flags FROM contact WHERE id = %s""",objid[0])
        fabuser = c.fetchone()
        if fabuser is not None:
            print fabuser
            name = fabuser[0] + " " + fabuser[1]
            print name
            access = fabuser[2] & binid
            activestatus = fabuser[2] & 512
            techaccess = fabuser[2] & techflag
            print "Access Flag: ", access
            print "Active Status: ", activestatus
            print "Tech Flag:   ",techaccess
            
            if ((access > 0) and (activestatus > 0)) or ((techaccess > 0) and (activestatus > 0)):
                
                #Start FabLab Status Check:
                c.execute("""SELECT status FROM fabstatus WHERE machine = %s""", ("fablab"))
                labstatus = c.fetchone()
                if (labstatus[0] == 1) or (techaccess > 0):
                    print "Fablab is Open"
                    lcd.clear()
                    lcd.backlight(lcd.GREEN)
                    lcd.message("FABLab is OPEN")
                    sleep(.5)
                    lcd.backlight(lcd.ON)

                    #Start Machine Status Check:
                    c.execute("""SELECT * FROM fabstatus WHERE machine = %s""", (hostname))
                    machineresult = c.fetchone()
                    machinestatus = machineresult[3]
                    if (machinestatus == 1) or (techaccess > 0):
                        print "%s is available" %hostname
                        lcd.backlight(lcd.GREEN)
                        lcd.message("\n%s is OPEN" %hostname)
                        sleep(.5)

                        #Grant or Deny Access:
                        try:
                            logBit = 1
                            facility = 1
                            logtime = strftime("%Y-%m-%d %H:%M:%S")                                 #Set up timestamp for visit logs
                            
                            start_time = time.time()
                            #Log the time of the barcode scan:
                            c.execute(("""INSERT INTO visitlog (id, member, logtime, logcode, \
                            organisation, facility, location, hostname, terminal, software, operator) \
                            values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""),\
                            (id, objid[0], logtime, logBit, organisation, facility, location, hostname, terminal, software, operator))
                            db.commit()

                            #This line sets the machine as IN USE by the current user:
                            c.execute("""UPDATE fabstatus SET status = 2, contactid = %s, name = %s WHERE machine = %s""", (objid[0], name, hostname))                                  
                            db.commit()

                            #Lastly, turn on the relay
                            GPIO.output(12, GPIO.HIGH)
                            print "Logged SUCCESS to database"
                            lcd.clear()
                            lcd.backlight(lcd.GREEN)
                            lcd.message("%s" % (name))
                            sleep(.5)
                            
                            c.close() #Close Connection in case of auto-logout
                            
                            
                            #Wait for user to log out
                            raw_input("PRESS ENTER TO LOG OUT ->")
                            
                            try:
                                lcd.clear()
                                lcd.backlight(lcd.YELLOW) #Sets LCD Warning mode
                                lcd.message("Accessing FABLab")
                                sleep(.2)
                                db=mdb.connect(host,user,password,database); #Tries connection to database
                                c = db.cursor() #Creates cursor object if successful
                            
                            except mdb.Error, e: #DB connection error handling
                                lcd.clear()
                                lcd.backlight(lcd.VIOLET)
                                lcd.message("SERVER NOT FOUND\nRESTART SCANNER")
                                break    

                            #Reset log status to log-out
                            logBit = 2
                            facility = 1
                            logtime = strftime("%Y-%m-%d %H:%M:%S")                                 #Set up timestamp for visit logs
                            c.execute(("""INSERT INTO visitlog (id, member, logtime, logcode, \
                            organisation, facility, location, hostname, terminal, software, operator) \
                            values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""),\
                            (id, objid[0], logtime, logBit, organisation, facility, location, hostname, terminal, software, operator))
                            db.commit()

                            #Resets the machine to available by the current user:
                            c.execute("""UPDATE fabstatus SET status = %s, contactid = 0, name = '' WHERE machine = %s""", (machinestatus,hostname))                                  
                            db.commit()
                            
                            elapsed_time = time.time() - start_time
                            fabvisitdate = strftime("%Y-%m-%d %H:%M:%S")
                            
                            #The following inserts a single line visit duration to the custom fabvisit table
                            c.execute(("""INSERT INTO fabvisit (id, member, machine, dateout, duration) values (%s, %s, %s, %s, %s)"""),\
                            (id, objid[0], hostname, fabvisitdate, elapsed_time))
                            db.commit()

                            #Lastly, turn off the relay
                            GPIO.output(12, GPIO.LOW)
                            print "Logged out of database"
                            print "Duration of visit:  %s" %elapsed_time
                            c.close()
                                                
                        except mdb.ProgrammingError:
                            print "DATABASE ERROR!"
                            pass
                            db.rollback()

                    #Machine access level - use codes to set status:                
                    elif (machinestatus == 2):                            #Checks for current usage
                        print "%s is IN USE" %hostname
                        lcd.clear()
                        lcd.backlight(lcd.RED)
                        lcd.message("%s\nis in use" % (hostname))
                        sleep(5)
                        c.close()
                        
                    elif (machinestatus == 3):                            #Checks for repair tag
                        print "%s is under repair" %hostname
                        lcd.clear()
                        lcd.backlight(lcd.RED)
                        lcd.message("%s\nis under repair" % (hostname))
                        sleep(5)
                        c.close()
                        
                    else:                                               #Checks if machine is offline
                        print "%s is offline" %hostname
                        lcd.clear()
                        lcd.backlight(lcd.RED)
                        lcd.message("%s\nis offline" % (hostname))
                        sleep(5)
                        c.close()
                        
                #Lab access level    
                else:
                    print "FabLab is closed"
                    lcd.clear()
                    lcd.backlight(lcd.RED)
                    lcd.message("FABLab is closed")
                    sleep(5)
                    c.close()
   
            #User access level failure
            else:
                lcd.clear()
                lcd.backlight(lcd.RED)
                lcd.message("Access Denied!\nSee a Lab Tech")
                print "Access Denied! See a Lab Tech"
                #Log scan without triggering GPIO
                logBit = 0
                facility = 0
                logtime = strftime("%Y-%m-%d %H:%M:%S")                                 #Set up timestamp for visit logs
                c.execute(("""INSERT INTO visitlog (id, member, logtime, logcode, \
                organisation, facility, location, hostname, terminal, software, operator) \
                values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""),\
                (id, objid[0], logtime, logBit, organisation, facility, location, hostname, terminal, software, operator))
                db.commit()
                c.close()
                sleep(5)
                
        #Error handling for failed code lookup
        else:
            lcd.clear()
            lcd.backlight(lcd.RED)
            lcd.message("User does\nNOT exist!")
            print "User does not exist!"
            sleep(5)
            c.close()
                
    #User exist level failure
    else:
        lcd.clear()
        lcd.backlight(lcd.RED)
        lcd.message("User does\nNOT exist!")
        print "User does not exist!"
        sleep(5)
        c.close()

"""NOTES"""
#1
"""The User is set via the hostname of the Pi itself.
To change the hostname:
edit both /etc/hosts and /etc/hostname to the new name (matching a device
in fabstatus) and reboot."""

#2
"""Current connection issues to database - need to debug"""
#3
#4

