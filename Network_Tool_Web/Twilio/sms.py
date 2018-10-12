"""
This script test a device using ICMP, if the host id Down it send a SMS to my phone.

"""

from twilio.rest import Client
import time
import datetime
import subprocess

account_sid = "AC41c1c9e2b0256753ef465b644516ba96"
auth_token = "7bb235fdb41bed95eec12997994bb6d0"
client = Client(account_sid, auth_token)

starttime = time.time()


def heartbeat():

    while True:

        try:

            subprocess.check_output(["ping", "-c", "1", "10.240.0.154"])
            time.sleep(2)
            print('Host is UP! at %s' % datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

        except Exception:

            print('')
            print('Host Down')
            print('')
            message = client.messages.create(
                to="+17873125359",
                from_="+17873362125",
                body="Router Stopped Responding Ping.")

            print('SMS Send to phone')
            print(message.sid)
            exit()


if __name__ == '__main__':

    heartbeat()
