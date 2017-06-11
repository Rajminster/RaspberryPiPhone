from glob import glob
from os.path import dirname, join

import kivy
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.properties import ObjectProperty, StringProperty, Logger
from kivy.uix.boxlayout import BoxLayout

# kivy.require('1.0.6')  # replace with your current kivy version !

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import AsyncImage, Image
from kivy.uix.label import Label


class HomeScreenApp(App):
    def build(self):
        # the root is created in pictures.kv
        root = GridLayout(cols=3)
        root.spacing = [10,-300]
        Window.size = (480, 800)
        Window.fullscreen = False

        # get any files into images directory
        curdir = dirname(__file__)
        for filename in glob(join(curdir, 'home_UI', '*')):
            try:
                # load the image
                image = Image(source=filename, allow_stretch=False)
                image.size = [0.5,0.5]
                # add to the main field
                root.add_widget(image)
            except Exception as e:
                Logger.exception('Pictures: Unable to load <%s>' % filename)
        return root


if __name__ == '__main__':
    home = HomeScreenApp()
    home.run()
