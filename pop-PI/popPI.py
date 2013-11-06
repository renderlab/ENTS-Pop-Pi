#!/usr/bin/python
# -*- coding: utf-8 -*-

from time import sleep
import RPi.GPIO as GPIO
import MySQLdb as mdb
import sys
import serial
RFID = ''
GPIO.setmode(GPIO.BCM)
#enable the gpio
GPIO.setup(18, GPIO.OUT)
#set the initial state
GPIO.output(18, False)

ser = serial.Serial('/dev/ttyAMA0', 2400, timeout=0.5)
while True:
	ser.open()
        RFID = ""
        RFID = ser.read(12)
        
        if len(RFID) != 0:
          ser.flushInput()
          ser.flushOutput()
          ser.close()
          print "RFID Read: " + RFID
		#Tag read
        
          try:
           con = mdb.connect('localhost', 'root', 'pi', 'pop_PI');
           with con:
            cur = con.cursor()

            cur.execute("SELECT 1 from MemberAccount where RFID = '%s'" % RFID )
            memberFound = cur.fetchone()
            if memberFound > 0:
                print "Member Found"
                cur.execute("SELECT Account from MemberAccount where RFID = '%s'" % RFID )

                account = cur.fetchone()
				#does the member have a positive balance 
                if account > 0:
                        sleep(1)
                        GPIO.output(18, False)
                        sleep(1)
                        GPIO.output(18, True)
                        sleep(1)
                        GPIO.output(18, False)
						#update the members balance
                        cur.execute("Update MemberAccount set Account = Account -1 where RFID = '%s'" % RFID)
                        cur.execute("SELECT Account from MemberAccount where RFID = '%s'" % RFID )
                        account = cur.fetchone()
                        print "Member new Account balance is : %s " % account
                        sleep(2)
        #               ser.open()
            else:
				#create new member
                print "Member Not Found Create"
                cur.execute("insert into MemberAccount (RFID,Account)values('%s',0)" % RFID)
                cur.execute("SELECT Account from MemberAccount where RFID = '%s'" % RFID )
                account = cur.fetchone()

                print "Member Account balance is : %s " % account
            sleep(1) #sleep for 5 seconds to prevent rfid reading
            ser.open()
            ser.flushInput()
            ser.flushOutput()
            sleep(1)

          except mdb.Error, e:

                print "Error %d: %s" % (e.args[0],e.args[1])
                sys.exit(1)

          finally:
                ser.close()
                if con:
                        con.close()
GPIO.cleanup()
