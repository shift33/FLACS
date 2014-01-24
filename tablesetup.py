#!/usr/bin/env python
#*- coding: utf-8 -*-

"""tablesetup.py creates the fabstatus and fablogin tables"""

__author__ = "Dan Wald"
__copyright__ = "Copyright 2014, UWStout FABLab"
__credits__ = ["Dan Wald", "Sam Armstrong"]
__license__ = "GPL"
__version__ = "0.4.0"
__maintainer__ = "Dan Wald"
__email__ = "waldd@my.uwstout.edu"
__status__ = "Prototype"

import MySQLdb as mdb
import sys
import socket
from time import strftime
from time import sleep

host = "192.168.1.145"                                                  #Database host
user = "root"                                                           #Database user
password = "wakibob24"                                                  #Database password
database = "FabControl"                                                 #Database tables

while (True):
    try:
        print "Connecting to Database..."
        db = mdb.connect(host,user,password,database);                  #Tries connection to database
        c = db.cursor()                                                 #Creates cursor object if successful
        print "Success!!"
        print ""
        break
    except MySQLdb.Error, e:                                            #DB connection error handling
        dbc = dbc + 1
        continue

print "Creating Table fabstatus2"
c.execute("""CREATE TABLE fabstatus2 (
   id INT NOT NULL AUTO_INCREMENT,
   binid INT(20),
   machine VARCHAR(11),
   hmachine VARCHAR(16),
   status INT(1),
   userid INT(11),
   PRIMARY KEY ( id )
);""")
db.commit()

print "Success!"
print "Inserting data variables"

c.execute("""INSERT INTO fabstatus (id, binid, machine, hmachine, \
status, userid) VALUES (%s, %s, %s, %s, %s, %s)""",\
[
(0,0,"fablab","FabLab",0,0),
#Skip binid 1, as it tests for tech flag
(0,2,"laser1","FabLab",0,0),
(0,4,"laser2","FabLab",0,0),
(0,8,"vinyl","FabLab",0,0),
(0,16,"3dprinter","FabLab",0,0),
(0,32,"shopbot","FabLab",0,0),
(0,64,"modellasmall","FabLab",0,0),
(0,128,"modellalarge","FabLab",0,0),
(0,256,"plasma","FabLab",0,0),
(0,512,"computers","FabLab",0,0)
#(0,1024,"","",0,0),
#(0,2048,"","",0,0),
#(0,4096,"","",0,0),
#(0,8192,"","",0,0),
#(0,16384,"","",0,0),
#(0,32768,"","",0,0),
#(0,65536,"","",0,0),
#(0,131072,"","",0,0),
])

db.commit()
