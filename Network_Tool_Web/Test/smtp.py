import smtplib

sender = 'rrivera@worldnetpr.com'
receivers = ['rllavona13@me.com']

message = """From: From Person <from@fromdomain.com>
To: To Person <to@todomain.com>
Subject: SMTP e-mail test

This is a test e-mail message.
"""

try:
    smtpObj = smtplib.SMTP('west.exch030.serverdata.net')
    smtpObj.sendmail(sender, receivers, message)
    print "Successfully sent email"

except Exception:
    print("Error: unable to send email")