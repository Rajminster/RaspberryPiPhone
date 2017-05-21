#!/usr/bin/python
# camera.py

from io import BytesIO
from os import environ, remove
from picamera import PiCamera
from subprocess import Popen
from sys import exit

WIDTH = 480 # width of the screen
HEIGHT = 800 # height of the screen

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
        self.rgb = bytearray(WIDTH * HEIGHT * 3)

    def display(self):
        while True:
            stream = BytesIO()
            self.camera.capture(stream, use_video_port = True, format = 'rgb')
            stream.seek(0)
            stream.readinto(self.rgb)
            stream.close()
            image = pygame.image.frombuffer(self.rgb[0:(WIDTH * HEIGHT * 3)], (WIDTH, HEIGHT), 'RGB')
            self.screen.blit(image, (0, 0))
            pygame.display.update()
