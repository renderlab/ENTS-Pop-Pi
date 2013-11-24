import RPi.GPIO as GPIO
from time import sleep

def creditPop()
	sleep(1)
	GPIO.output(23, False)
	sleep(1)
	GPIO.output(23, True)
	sleep(1)
	GPIO.output(23, False)