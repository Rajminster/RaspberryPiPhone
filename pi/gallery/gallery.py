import kivy
from kivy.lang import Builder
from kivy.logger import Logger
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.carousel import Carousel
from kivy.uix.image import AsyncImage

# kivy.require('1.0.6')  # replace with your current kivy version !

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label
from os.path import dirname, join

from setuptools.glob import glob


class GalleryApp(App):
    def build(self):
        carousel = Carousel(direction='right')
        # get any files into images directory
        curdir = dirname(__file__)
        for filename in glob(join(curdir, 'DCIM', '*')):
            image = AsyncImage(source=filename, allow_stretch=True)
            carousel.add_widget(image)
        return carousel
        #return BoxLayout()


def main():
    home = GalleryApp()
    home.run()


if  __name__ =='__main__':main()

