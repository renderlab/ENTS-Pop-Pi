from time import sleep
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
#old pin 18
GPIO.setup(23, GPIO.OUT)
GPIO.output(23, False)
sleep(1)
GPIO.output(23, True)
sleep(1)
GPIO.output(23, False)
GPIO.cleanup()



GPIO.setup(18,GPIO.OUT)
#GPIO.output(18,False)
sleep(1)
GPIO.output(18,True)
sleep(1)
GPIO.output(18,False)
sleep(1)
GPIO.cleanup()


