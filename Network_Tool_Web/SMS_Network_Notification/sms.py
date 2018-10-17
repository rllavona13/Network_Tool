"""
This script can be used as a notification service

For example:
    This script use the command ping with 1 count to an Router IP Address.
    If the ping is successful if will try again every 2 seconds and if fail
    it will print out that the host is down and will send an SMS to my personal
    cell phone.

It can be used in any shell command or any other implementation.

"""

from twilio.rest import Client
import time
import datetime
import subprocess

account_sid = "AC41c1c9e2b0256753ef465b644516ba96"
auth_token = "7bb235fdb41bed95eec12997994bb6d0"
client = Client(account_sid, auth_token)

system_time = time.time()


def heartbeat():

    while True:

        try:

            subprocess.check_output(['ping', '-c', '1', '10.240.0.154'])
            time.sleep(2)
            print('Host is UP! at %s' % datetime.datetime.now().strftime('%m-%d-%Y %H:%M:%S'))

        except Exception:

            print('')
            print('Host Down')
            print('')
            message = client.messages.create(
                to="+17873125359",
                from_="+17873362125",
                body="Router Stopped Responding Ping.")
            print('')
            print('SMS Send to phone')
            print(message.sid)
            exit()


if __name__ == '__main__':

    heartbeat()
