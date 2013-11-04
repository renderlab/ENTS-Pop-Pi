from time import sleep
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
#enable the gpio
GPIO.setup(18, GPIO.OUT)
#set the initial state
GPIO.output(18, False)
sleep(1)
#turn the relay on
GPIO.output(18, True)
sleep(1)
#turn the relay off.
GPIO.output(18, False)