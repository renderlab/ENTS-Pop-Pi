import urllib2

response = urllib2.urlopen('http://api.thingspeak.com/update?key=HCT8075Y1EDGTU7T&field1=0&field2=0&field3=0&field4=0&field5=0&field6=0&field7=0&field8=0')
html = response.read()


