from time import sleep
import serial
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(18,GPIO.OUT)

ser = serial.Serial('/dev/ttyAMA0', 2400, timeout=0.5)
GPIO.output(18,True)
while True:
        GPIO.output(18,False)
        string = ser.read(12)
        GPIO.output(18,True)
        if len(string) != 0:
          ser.close()
          print string
          sleep(5)
          ser.open()

GPIO.cleanup()

