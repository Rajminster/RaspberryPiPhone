#!/usr/bin/python
# camera.py

from io import BytesIO
from os import environ, remove
from picamera import PiCamera
from subprocess import Popen
from sys import exit
from time import sleep
from datetime import datetime, timedelta

WIDTH = 480 # width of the screen
HEIGHT = 800 # height of the screen
bool buttonHit = False

class App():
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
        self.rgb = bytearray(WIDTH * HEIGHT * 3)]

    def save_file(self, filename):


    def display(self):
        while True:
            # self.camera.resolution = (1024, 768)

            stream = BytesIO()
            self.camera.capture(stream, use_video_port = True, format = 'rgb')
            stream.seek(0)
            stream.readinto(self.rgb)
            stream.close()
            image = pygame.image.frombuffer(self.rgb[0:(WIDTH * HEIGHT * 3)], (WIDTH, HEIGHT), 'RGB')
            self.screen.blit(image, (0, 0))
            pygame.display.update()

    def record(self):
        # self.camera.resolution = (640, 480)
        self.camera.start_recording('my_video.h264')
        if (buttonHit):
            self.camera.stop_recording()
        close(self)


    def lowLightImage(self):
        # camera.resolution = (1280, 720)
        # Set a framerate of 1/6fps, then set shutter
        # speed to 6s and ISO to 800
        self.camera.framerate = Fraction(1, 6)
        self.camera.shutter_speed = 6000000
        self.camera.exposure_mode = 'off'
        self.camera.iso = 800
        # Give the camera a good long time to measure AWB
        # (you may wish to use fixed AWB instead)
        sleep(10)
        # Finally, capture an image with a 6s exposure. Due
        # to mode switching on the still port, this will take
        # longer than 6 seconds
        self.camera.capture('dark.jpg')
        close(self)

    def wait():
        # Calculate the delay to the start of the next hour
        next_hour = (datetime.now() + timedelta(hour=1)).replace(
        minute=0, second=0, microsecond=0)
        delay = (next_hour - datetime.now()).seconds
        sleep(delay)

    def timelapse(self):


        self.camera.start_preview()
        wait()
        for filename in self.camera.capture_continuous('img{timestamp:%Y-%m-%d-%H-%M}.jpg'):
            print('Captured %s' % filename)
            wait()
        close(self)

    def image(self):
        self.camera.start_preview()
        # Camera warm-up time
        sleep(2)
        self.camera.capture('foo.jpg')
        close(self)

    def flash(self):
        self.camera.flash_mode = 'on'
        self.camera.capture('whatever.jpg')
        close(self)


    def close(self):
        self.camera.close()
