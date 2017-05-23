#!/usr/bin/python
# camera.py

from io import BytesIO
from os import environ, remove
from picamera import PiCamera
from subprocess import Popen
from sys import exit
from time import sleep
from datetime import datetime, timedelta

class Camera():
    """Wrapper class to interact with the Raspberry Pi's camera hardware
    in order to capture and save photos as well as record videos.
    
    Attributes:
        WIDTH (int): width of the touch screen
        HEIGHT (int): height of the touch screen
        buttonHit (boolean): boolean flag used whenever a button has been pressed in the UI
    """

    WIDTH = 480
    HEIGHT = 800
    buttonHit = False
    
    def __init__(self):
        # set screen to SPI
        environ['SDL_FDBEV'] = '/dev/fb1'
        environ['SDL_MOUSEDEV'] = '/dev/input/touchscreen'
        environ['SDL_MOUSEDRV'] = 'TSLIB'

        # configure camera
        self.camera = PiCamera()
        self.camera.resolution = (WIDTH, HEIGHT)
        self.camera.rotation = 180

        # buffers for viewfinder data
        self.rgb = bytearray(WIDTH * HEIGHT * 3)

    def save_file(self, file_name):
        """Save an image file
        
        Arg:
            file_name (str): name of the file including the file extension.
        """
        f = open('../photos/' + file_name, 'w+')
        f.close()

    def display(self):
        """Method to display on the screen what the camera "sees"."""
        while True:
            # self.camera.resolution = (1024, 768)
            stream = BytesIO()
            self.camera.capture(stream, use_video_port=True, format='rgb')
            stream.seek(0)
            stream.readinto(self.rgb)
            stream.close()
            """
            image = pygame.image.frombuffer(self.rgb[0:(WIDTH * HEIGHT * 3)], (WIDTH, HEIGHT), 'RGB')
            self.screen.blit(image, (0, 0))
            pygame.display.update()
            """

    def record(self):
        # self.camera.resolution = (640, 480)
        self.camera.start_recording('my_video.h264')
        if (buttonHit):
            self.camera.stop_recording()

    def lowLightImage(self):
        # camera.resolution = (1280, 720)
        """Set a framerate of 1/6fps, then set shutter speed to 6s and ISO to 800"""
        self.camera.framerate = Fraction(1, 1)
        self.camera.shutter_speed = 1000000
        self.camera.exposure_mode = 'off'
        self.camera.iso = 800
        # Give the camera a good long time to measure AWB
        # (you may wish to use fixed AWB instead)
        sleep(10)
        # Finally, capture an image with a 6s exposure. Due
        # to mode switching on the still port, this will take
        # longer than 6 seconds
        self.camera.capture('dark.jpg')

    def wait():
        """Calculate the delay to the start of the next hour"""
        next_hour = (datetime.now() + timedelta(hour=1)).replace(minute=0, second=0, microsecond=0)
        delay = (next_hour - datetime.now()).seconds
        sleep(delay)

    def timelapse(self):
        self.camera.start_preview()
        wait()
        for filename in self.camera.capture_continuous('img{timestamp:%Y-%m-%d-%H-%M}.jpg'):
            print('Captured %s' % filename)
            self.wait()

    def image(self):
        self.camera.start_preview()
        # Camera warm-up time
        sleep(2)
        self.camera.capture('foo.jpg')

    def flash(self):
        """Enables the Raspberry Pi's camera's flash."""
        self.camera.flash_mode = 'on'

    def close(self):
        """Method called whenever the camera UI is closed. Closes the Raspberry Pi's camera."""
        self.camera.close()
