#!/usr/bin/env python
#-*- coding: utf-8 -*-
#
# v0.2.2 FLACS
# Dan Wald

import MySQLdb as mdb
import sys
import socket
from time import strftime
try:
    import RPi.GPIO as GPIO
except RunTimeError:
    print ("Must run as ROOT! - Try using SUDO!")

#These variables control the Database connection
#The User is set via the hostname of the Pi itself
#To change the hostname:
#edit both /etc/hosts and /etc/hostname to the new name
#To take effect, reboot the system

#Connect to database:
user = socket.gethostname()
db=mdb.connect("144.13.119.113",user,"password","FabControl");
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

#Uncomment if the auto-incriment in MySQL does not work:
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
            x = int(raw_input("SCAN BARCODE: "))
        except ValueError:
            print "Not A Valid User! Must be number in format XXXXXX."
            print ""
            continue
        else:
            return (x)
logtime = strftime("%Y-%m-%d %H:%M:%S")

#Return database version:
c.execute("SELECT VERSION()")
ver=c.fetchone()
print "DB Version: %s" % ver

#Begin program loop
while (True):
    print ""
    barcode=scan()
    
    #Start FabLab Status Check:
    c.execute("""SELECT status FROM fabstatus WHERE machine = %s""", ("fablab"))
    labstatus = c.fetchone()
    if labstatus[0] == 1:
        print "Fablab is Open"

        #Start Machine Status Check:
        c.execute("""SELECT * FROM fabstatus WHERE machine = %s""", (hostname))
        machineresult = c.fetchone()
        machinestatus = machineresult[3]
        binid = machineresult[1]
        if machinestatus == 1:
            print "%s is available" %hostname

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

                #Grant or Deny Access:
                if access > 0:
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
                        
                #User access level
                else:
                    print "Access Denied! Please See a Lab Tech"
                    #Log scan without triggering GPIO - set 
                    logBit = 0
                    facility = 0
                    c.execute(("""INSERT INTO visitlog (id, member, logtime, logcode, \
                    organisation, facility, location, hostname, terminal, software, operator) \
                    values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""),\
                    (id, fabuser[2], logtime, logBit, organisation, facility, location, hostname, terminal, software, operator))
                    db.commit()
                    
            #User exist level
            else:
                print "User does not exist!"
            
        #Machine access level - use codes to set status:
                
        elif machinestatus == 2:
            print "%s is IN USE" %hostname
            
        elif machinestatus == 3:
            print "%s is under repair" %hostname
            
        else:
            print "%s is offline" %hostname
            
    #Lab access level    
    else:
        print "FabLab is closed"

    
    

    
    





