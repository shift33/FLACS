#!/usr/bin/python
#-*- coding: utf-8 -*-
import MySQLdb as mdb
import sys
machines = ("","FABLAB","Lasers","Vinyl Cutter",
"3D Printer","ShopBot","Mini Mills","Plasma")
machinenumber = (0,1,2,4,8,16,32,64)
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
while (True):
    barcode = scan()
    machine = 1
    db=mdb.connect(
        host="192.168.2.4",
        user="FabControl",
        passwd="fablab",
        db="FabControl",);
    c=db.cursor()
    c.execute("""SELECT objid FROM scancode WHERE code = %s""",(barcode,))
    result=c.fetchone()
    if result is not None:
        print "UserID: ", result[0]
        c.execute("""SELECT name, surname, flags FROM contact WHERE id = %s""",
        (result[0],))
        result2=c.fetchone()
        if result2 is not None:
            print "Name: ", result2[0], result2[1]
            print "Flags: ", result2[2]
            print ""
            flag=int(result2[2])
            for z in range(1,8):
                access = flag & machinenumber[machine]
                if access > 0:
                    print textcolor.OKGREEN + "Access GRANTED to",machines[machine] + textcolor.ENDC
                    print ""
                else:
                    print textcolor.FAIL + "Access DENIED to",machines[machine] + textcolor.ENDC
                    print ""
                machine=machine+1
        else:
            print "DB ERROR"
        db.close()
    else:
        print textcolor.FAIL + "NOT A VALID USER" + textcolor.ENDC
        print ""
        db.close()
