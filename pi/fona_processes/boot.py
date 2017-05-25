#!/usr/bin/env python
# boot.py

from call_thread import Call_Thread
from sms_thread import SMS_Thread
from threading import Lock

__author__ = "Nikola Istvanic"
__date__ = "2017-05-24"
__version__ = "1.0"

"""Script to run whenever the Raspberry Pi is booted to create background
threads which check for when a call or message has been received."""

if __name__ == '__main__':
    sLock = Lock()
    Call_Thread(sLock).start()
    SMS_Thread(sLock).start()
