#!/usr/bin/python
#-*- coding: utf-8 -*-
import MySQLdb as mdb
import sys
from time import strftime
try:
    import RPi.GPIO as GPIO
	import Settings
	import FuncLib as FUNC
except RunTimeError:
    print("Must run as Root! - Try Using SUDO")

 c = FUNC.connectDatabase(Settings.host(),Settings.user(),
						  Settings.passwd(),Settings.db())

machine = 0	
	

#GPIO Pin Housekeeping

GPIO.setmode(GPIO.BOARD)  #Sets Pinout numbering to 1-26
GPIO.setup(12, GPIO.OUT)  #Sets PIN 12 (BCM 18) to Output
GPIO.output(12, GPIO.LOW) #Sets initial value to off


#Check and return database version
print ""
c.execute("SELECT VERSION()")
ver = c.fetchone()
print textcolor.OKBLUE + "Database Version : %s " % ver + textcolor.ENDC
print ""


#CORE PROGRAM
while (True):

    barcode = FUNC.scan() #Input barcode
	objidResult = FUNC.objidGet(c,barcode) #Returns recordset of objid based on barcode
	if objidResult is not None:
		
		member = objidResult[0]#Set the correct result to the member var
		flagsAndNameResult = FUNC.flagsAndNameGet(c,objidResult[0])#Attempt to get the flags and name based on objid
		binid = binidGet(c,Settings.hostname())
		
		if flagsAndNameResult is not None:
			print "Name: ", flagsAndNameResult[0], flagsAndNameResult[1]
			print "Flags: ", flagsAndNameResult[2]
			print "Machine: ", Settings.hostname(), "-", binid[0]
			

			flag=int(flagsAndNameResult[2])
			access = flag & binid[0]
			if access > 0:
				print '\033[92m' + "Access GRANTED to " + Settings.hostname() + '\033[0m'
				print ""
				

				try:
					FUNC.logContact(c,Settings.id(),member,
									1,Settings.organisation(),Settings.facility(),
									Settings.location(),Settings.hostname(),
									Settings.terminal(),Settings.software(),
									Settings.operator(),)
									
					GPIO.output(12, GPIO.HIGH) #Fire the Relay
					
					#REPLACE THIS LINE WITH BUTTON HOOK FROM GPIO
					raw_input("Press ENTER to log out -> ")

					FUNC.logContact(c,Settings.id(),member,
									0,Settings.organisation(),Settings.facility(),
									Settings.location(),Settings.hostname(),
									Settings.terminal(),Settings.software(),
									Settings.operator(),)
									
					GPIO.output(12, GPIO.LOW) #Disable the Relay
				except mdb.ProgrammingError:
					pass
					db.rollback()
			else:
				print '\033[91m' + "Access DENIED to" Settings.hostname() + '\033[0m'
				print ""
		else:
			print "DB ERROR"
	else:
		print '\033[91m' + "NOT A VALID USER" + '\033[0m'
		print ""

    
