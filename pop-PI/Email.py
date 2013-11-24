#http://www.raspberrypi-spy.co.uk/2012/05/send-text-and-html-email-using-python/
# Import smtplib to provide email functions
import smtplib

# Import the email modules
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import MySQLdb as mdb

def emailMember(RFID):
	# Define email addresses to use
	con = mdb.connect('localhost', 'root', 'pi', 'pop_PI');
	with con:
		cur = con.cursor()
		cur.execute("SELECT Email from MemberAccount where RFID = '%s'" % RFID )

		addr_to = cur.fetchone()
		cur.execute("select Account from MemberAccount where RFID = '%s'" % RFID)
		
		balance = cur.fetchone() # retrieve balance from the account
		addr_from = 'pop.pi@ents.ca'
		if addr_to > 0:
			# Define SMTP email server details
			smtp_server = 'smtp.gmail.com:587'
			smtp_user   = 'pop.pi@ents.ca'
			smtp_pass   = 'knockknockknockpenny'

			# Construct email
			msg = MIMEMultipart('alternative')
			msg['To'] = addr_to
			msg['From'] = addr_from
			msg['Subject'] = 'Test Email From RPi'

			# Create the body of the message (a plain-text and an HTML version).
			text = "This is a test message.\nText and html."
			html = """\
			<html>
			  <head></head>
			  <body>
				<h1>Your Account Balance Is.</h1>
				<p><h1>d%</h1></p>
				<p>To top up your account visit poppi.ents.ca</p>
			  </body>
			</html>
			""" % balance
			

			# Record the MIME types of both parts - text/plain and text/html.
			part1 = MIMEText(text, 'plain')
			part2 = MIMEText(html, 'html')
			# Attach parts into message container.
			# According to RFC 2046, the last part of a multipart message, in this case
			# the HTML message, is best and preferred.
			msg.attach(part1)
			msg.attach(part2)

			# Send the message via an SMTP server
			s = smtplib.SMTP(smtp_server)
			s.starttls()
			s.login(smtp_user,smtp_pass)
			s.sendmail(addr_from, addr_to, msg.as_string())
			s.quit()
			
		if con:
			con.close()