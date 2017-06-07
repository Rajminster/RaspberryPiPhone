#!/usr/bin/env python

from call_thread import Call_Thread
from sms_thread import SMS_Thread
from ui_thread import UI_Thread
from threading import Lock

__author__ = 'Nikola Istvanic'
__date__ = '2017-05-30'
__version__ = '1.0'

"""Script to run whenever the Raspberry Pi is booted to create background
threads to check FONA device for incoming calls or SMSs.

At the time of the Raspberry Pi's boot, the operations of the mobile telephone
(calling, messaging, UI appearance) must start. This scripts accomplishes this
task by creating three threading.Lock objects.

fona_lock is a lock object which controls thread access to the FONA device
serial port. This lock is required by all threads (call, sms, and UI) because
each thread at some point will send a command to the FONA device.

call_lock and sms_lock are both used to limit one thread to write to a text file
located either in the phone or message directory.

When this script runs, three threads are created: one for polling the FONA for
incoming calls, one for polling the FONA for incoming SMSs, and one for setting
up and displaying the UI.
"""

if __name__ == '__main__':
    fona_lock = Lock()
    call_lock = Lock()
    sms_lock = Lock()
    Call_Thread(fona_lock, call_lock).start()
    SMS_Thread(fona_lock, sms_lock).start()
    UI_Thread(fona_lock, call_lock, sms_lock).start()
