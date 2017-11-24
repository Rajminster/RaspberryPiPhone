#!/usr/bin/env python3

from datetime import datetime
from signal_thread import Signal_Thread
from threading import Lock

import logging
import os

__author__ = 'Nikola Istvanic'
__date__ = '2017-05-30'
__version__ = '1.0'

"""Script to run whenever the Raspberry Pi is first booted to create background
threads which check the FONA device for incoming calls or SMSs.

At the time of the Raspberry Pi's boot, the operations of the mobile telephone
(calling, messaging, UI appearance, notifications) must start. This script
accomplishes this task by creating three threading.Lock objects which will be
used by each of the thread classes created in the core directory.

The first thread lock is fona_lock which will control thread access to the FONA
device serial port. This lock is required by all threads (call, sms, and signal)
because each thread at some point will send a command to the shared FONA device.

The next two are call_lock and sms_lock which limit one thread to write to a
text file located either in the phone or message directory.

When this script runs, three threads are created: one for polling the FONA for
incoming calls, one for polling the FONA for incoming SMSs, and responsible for
signalling to the UI of the OS that there is a phone call or SMS.
"""
if __name__ == '__main__':
    logger = logging.getLogger(__name__)
    if not os.path.isdir('logs'):
        logger.warn('Directory logs not found, creating directory')
        os.mkdir('logs')
    handler = logging.FileHandler(
        'logs/%s.log' % datetime.now().replace(microsecond=0))
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(module)s::'
        '%(funcName)s: %(message)s', '%Y-%m-%d %H:%M:%S %Z')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)
    ############################################################################
    # TODO: create GUI base here and pass that in as parameter to Signal_Thread#
    ############################################################################

    Signal_Thread(Lock(), Lock(), Lock()).start()
