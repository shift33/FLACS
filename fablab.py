#!/usr/bin/python
#-*- coding: utf-8 -*-
import MySQLdb as mdb
import sys
from time import strftime
try:
    import RPi.GPIO as GPIO
except RunTimeError:
    print("Must run as Root! - Try Using SUDO")


#GPIO Pin Housekeeping

GPIO.setmode(GPIO.BOARD)  #Sets Pinout numbering to 1-26
GPIO.setup(12, GPIO.OUT)  #Sets PIN 12 (BCM 18) to Output
GPIO.output(12, GPIO.LOW) #Sets initial value to off


#Base "machine" is set to the default FABLAB to prevent a restart attempt
machine = 0

machines = ("FABLAB","Lasers","Vinyl Cutter","3D Printer","ShopBot","Mini Mills","Plasma")
machinenumber = (0,1,2,4,8,16,32,64,128,256,512,1024,2048)

#Generic data for visitlogging
id = 0
organisation = 0
facility = 0
location = machines[machine]
hostname = "Pi #1"
terminal = 0
software = 20011
operator = 0

#MySQL Database variables
db=mdb.connect(
        host="192.168.2.4",
        user="FabControl",
        passwd="fablab",
        db="FabControl",
        );
c=db.cursor()

#Text color ONLY works in the terminal
class textcolor:
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    OKBLUE = '\033[94m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

    def disable(self):
        self.OKGREEN = ''
        self.WARNING = ''
        self.OKBLUE = ''
        self.FAIL = ''
        self.ENDC = ''

#Check and return database version
print ""
c.execute("SELECT VERSION()")
ver = c.fetchone()
print textcolor.OKBLUE + "Database Version : %s " % ver + textcolor.ENDC
print ""

#Define scanning for numbers only
def scan():
    while (True):
        try:
            x = int(raw_input(textcolor.OKBLUE + "BARCODE: " + textcolor.ENDC))
        except ValueError:
            print textcolor.FAIL + "NOT A VALID USER" + textcolor.ENDC
            print ""
            continue
        else:
            return (x)

#Define machine reset options for valid numbers
def machinereset():
    while (True):
        try:
            y = int(raw_input(textcolor.OKBLUE + "MACHINE NUMBER: " + textcolor.ENDC))
        except ValueError:
            print textcolor.FAIL + "NOT A VALID NUMBER" + textcolor.ENDC
            print ""
            continue
        else:
            return (y)
             
#CORE PROGRAM
while (True):

    barcode = scan() #Input barcode
    if barcode == 000000:
        print ""
        machine = machinereset()
        location = machines[machine]
        print machines[machine]
        print ""
    else:
        c.execute("""SELECT objid FROM scancode WHERE code = %s""",(barcode,))
        result=c.fetchone()
        if result is not None:
            print "UserID: ", result[0]
            c.execute("""SELECT name, surname, flags FROM contact WHERE id = %s""",
            (result[0],))
            member = result[0]
            
            result2=c.fetchone()
            if result2 is not None:
                print "Name: ", result2[0], result2[1]
                print "Flags: ", result2[2]
                print "Machine: ", machine, "-", machines[machine]
                

                flag=int(result2[2])
                access = flag & machinenumber[machine]
                if access > 0:
                    print textcolor.OKGREEN + "Access GRANTED to",machines[machine] + textcolor.ENDC
                    print ""
                    

                    try:
                        logtime = strftime("%Y-%m-%d %H:%M:%S")
                        logcode = 1
                        c.execute("""INSERT INTO visitlog (id, member, logtime,
                        logcode, organisation, facility, location, hostname,
                        terminal, software, operator)
                        values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                        (id, member, logtime, logcode, organisation,
                        facility, location, hostname, terminal, software, operator))
                        db.commit()
                        GPIO.output(12, GPIO.HIGH) #Fire the Relay
                        
                        #REPLACE THIS LINE WITH BUTTON HOOK FROM GPIO
                        raw_input("Press ENTER to log out -> ")

                        logtime = strftime("%Y-%m-%d %H:%M:%S")
                        logcode = 0
                        c.execute("""INSERT INTO visitlog (id, member,
                        logtime, logcode, organisation, facility, location,
                        hostname, terminal, software, operator)
                        values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                        (id, member, logtime, logcode, organisation,
                        facility, location, hostname, terminal, software, operator))
                        db.commit()
                        GPIO.output(12, GPIO.LOW) #Disable the Relay
                        


                        
                    except mdb.ProgrammingError:
                        pass
                        db.rollback()


                    
                else:
                    print textcolor.FAIL + "Access DENIED to",machines[machine] + textcolor.ENDC
                    print ""
            else:
                print "DB ERROR"
        else:
            print textcolor.FAIL + "NOT A VALID USER" + textcolor.ENDC
            print ""

    
