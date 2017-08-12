#!/usr/bin/env python

from threading import Lock

from signal_thread import Signal_Thread

__author__ = 'Nikola Istvanic'
__date__ = '2017-05-30'
__version__ = '1.0'

"""Script to run whenever the Raspberry Pi is booted to create background
threads to check FONA device for incoming calls or SMSs.

At the time of the Raspberry Pi's boot, the operations of the mobile telephone
(calling, messaging, UI appearance, notifications) must start. This scripts
accomplishes this task by creating three threading.Lock objects.

The first thread lock is fona_lock which controls thread access to the FONA
device serial port. This lock is required by all threads (call, sms, and signal)
because each thread at some point will send a command to the FONA device.

The next two are call_lock and sms_lock which limit one thread to write to a
text file located either in the phone or message directory.

When this script runs, three threads are created: one for polling the FONA for
incoming calls, one for polling the FONA for incoming SMSs, and responsible for
signalling to the UI of the OS that there is a phone call or SMS.
"""
if __name__ == '__main__':
    ###############################################################################
    # TODO: create entire GUI here and pass that in as parameter to Signal_Thread #
    ###############################################################################
    
    Signal_Thread(Lock(), Lock(), Lock()).start()
