#!/usr/bin/python
# -*- coding: utf-8 -*-

from time import sleep
import RPi.GPIO as GPIO
import MySQLdb as mdb
import sys
import serial
import Email
import PopRelay



RFID = ''
GPIO.setmode(GPIO.BCM)
#enable the gpio
GPIO.setup(23, GPIO.OUT)# output for relay
GPIO.setup(18, GPIO.OUT) # output for rfid enable
#set the initial state
GPIO.output(23, False)#old 18
GPIO.output(18, False)
Debug = True

ser = serial.Serial('/dev/ttyAMA0', 2400, timeout=0.5)

while True:
        ser.open()
        RFID = ""
        GPIO.output(18, False)
        RFID = ser.read(12)

        if len(RFID) != 0:
          GPIO.output(18, True)#rfid read pull the enable pin
          ser.flushInput()
          ser.flushOutput()
          ser.close()
          print "RFID Read: " + RFID
		#Tag read
          #print string
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
				#does the member have a positive account
                if (account > 0):
					PopRelay.creditPop()
					
					cur.execute("Update MemberAccount set Account = Account -1 where RFID = '%s'" % RFID)
					cur.execute("SELECT Account from MemberAccount where RFID = '%s'" % RFID )

					account = cur.fetchone()
					print "Member new Account balance is : %s " % account
					
					cur.execute("Insert PopVend (Pop) values (1)")
					cur.execute("Insert Inventory (Pop) values (-1)")
					cur.execute("Select count(Pop) from PopVend")
					popVendTotal = cur.fetchone()
					cur.execute("Select sum(pop) from Inventory")

					try:
						response = urllib2.urlopen('http://api.thingspeak.com/update?key=HCT8075Y1EDGTU7T&field2=%n&field3=%n' % (membercount, inventory)) #update thingspeak
						html = response.read()
					finally:
							#we tried

					#Notify the member of their account
					try:
                        Email.emailMember(RFID)
                    finally:
                        #we tried
					
					RFID = ""
					sleep(2)
					#ser.open()
				else
					#The Notify the member of their account
					try:
                        Email.emailMember(RFID)
                    finally:
                        #we tried

            else:
				#create new member
                print "Member Not Found Create"
                cur.execute("insert into MemberAccount (RFID,Account)values('%s',0)" % RFID)
                cur.execute("SELECT Account from MemberAccount where RFID = '%s'" % RFID )
                account = cur.fetchone()
                RFID = ""

                cur.execute("Select count(Account) from MemberAccount")
                membercount = cur.fetchone()
                try:
                    response = urllib2.urlopen('http://api.thingspeak.com/update?key=HCT8075Y1EDGTU7T&field1=%n' % membercount)
                    html = response.read()
                finally:
                    #we tried

                print "Member Account balance is : %s " % account
            sleep(1) #sleep for 5 seconds to prevent rfid
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
