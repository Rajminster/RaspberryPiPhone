from call_thread import Call_Thread
from sms_thread import SMS_Thread
from ui_thread import UI_Thread
from threading import Lock

__author__ = 'Nikola Istvanic'
__date__ = '2017-05-30'
__version__ = '1.0'

"""Script to run whenever the Raspberry Pi is booted to power GSM and create
background threads to check for when a call or message has been received."""

if __name__ == '__main__':
    fona_lock = Lock()
    call_lock = Lock()
    sms_lock = Lock()
    Call_Thread(fona_lock, call_lock).start()
    SMS_Thread(fona_lock, sms_lock).start()
    UI_Thread(fona_lock, call_lock, sms_lock).start()
