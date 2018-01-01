from glob import glob
from os.path import dirname, join

import kivy
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.properties import ObjectProperty, StringProperty, Logger
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout

# kivy.require('1.0.6')  # replace with your current kivy version !

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import AsyncImage, Image
from gallery.gallery import GalleryApp
from message.message import MessageApp
import multiprocessing

class HomeScreenApp(App):
    def build(self):
        uproot = BoxLayout()
        # the root is created in pictures.kv
        #root = GridLayout(cols=3)
        #root.spacing = [10,-300]
        root = FloatLayout()
        Window.size = (480, 800)
        Window.fullscreen = False

        # get any files into images directory
        #75 from left, 160 between
        x = 30
        y = 395
        col = 1

        button = HomeButton(size_hint=(.47, .47), pos=(216, 12))
        button.opacity = 0.1
        image = Image(source='Home_Button.png', allow_stretch=False, pos=(0,-365))
        root.add_widget(button)
        root.add_widget(image)

        curdir = dirname(__file__)
        for filename in glob(join(curdir, 'home_UI_icons', '*')):
            try:
                # load the image
                button = Button(size_hint=(.23, .132), pos=(x, y))
                image = Image(source=filename, allow_stretch=False)
                image.size = (120,120)
                button.add_widget(image)
                image.center = (button.center_x,button.center_y)
                # add to the main field
                root.add_widget(button)
                if col == 3:
                    col = 1
                    x = 30
                    y -= 140
                else:
                    x += 160
                    col += 1

            except Exception as e:
                Logger.exception('Pictures: Unable to load <%s>' % filename)
        uproot.add_widget(root)
        return uproot


class HomeButton(ButtonBehavior, Image):
    def __init__(self, **kwargs):
        super(HomeButton, self).__init__(**kwargs)

    def on_press(self):
        app = MessageApp()
        p = multiprocessing.Process(target=app.run)
        p.start()

    def on_release(self):
        pass


if __name__ == '__main__':
    home = HomeScreenApp()
    home.run()