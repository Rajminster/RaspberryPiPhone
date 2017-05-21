from call_thread import Call_Thread
from fona import power_gsm
from sms_thread import SMS_Thread
from threading import Lock

"""Script to run whenever the Raspberry Pi is booted to power GSM and create
background threads to check for when a call or message has been received."""

if __name__ == '__main__':
    power_gsm()
    sLock = Lock()
    Call_Thread(sLock).start()
    SMS_Thread(sLock).start()
