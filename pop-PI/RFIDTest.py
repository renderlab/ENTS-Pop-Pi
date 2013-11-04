import serial
ser = serial.Serial('/dev/ttyAMA0', 2400, timeout=0.5)
while True:
    string = ser.read(12)
    if len(string) == 0:
        print "Please insert a tag"
        continue
    else:
        string = string[1:11] #exclude start x0A and stop x0D bytes
        if string == '0415DB18A3':
            print "You used your black tag"
        elif string == '0F03028F57':
            print "You used your white tag"
        else:
            print "You do not have a valid tag"


