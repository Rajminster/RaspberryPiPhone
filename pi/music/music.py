import os
from Canvas import Rectangle

from kivy.core.window import Window
from kivy.graphics.instructions import Canvas
from kivy.uix.boxlayout import BoxLayout

from kivy.core.audio import SoundLoader
from kivy.uix.screenmanager import ScreenManager, Screen

# need to define clicked in UI
#sound = SoundLoader.load(clicked)


from kivy.app import App
from kivy.uix.carousel import Carousel
from kivy.uix.image import AsyncImage
from os.path import dirname, abspath

from kivy.uix.floatlayout import FloatLayout



class Sound():
    count = 0
    Songsplayed = 0
    d = dict()
    path = 'Users/Dharshan/Documents/RaspberryPiPhone/songs'
    for filename in os.listdir(path):
        d[count] = filename
        count = count + 1
    sound = SoundLoader.load(d.get(0))

    first = sound

    def play(self):
        if sound:
            sound.play()
    def pause(self):
        sound.stop()
    def playAtTime(self, time):
        sound.seek(time)

    def next(self):
        sound.unload()
        Songsplayed = Songsplayed + 1
        if Songsplayed > count - 1:
            sound = first
            Songsplayed = 0
        else:
            sound = SoundLoader.load(d.get(Songsplayed))
        play()


    def back(self):
        sound.unload()
        if (Songsplayed-1)%(count-1) == 0:
            sound = SoundLoader.load(d.get(count - 1))
        else:
            sound = SoundLoader.load(d.get((Songsplayed-1)%(count-1)))
        play()


class ListScreen(screen):
    def __init__(self, **kwargs):
        super(ListScreen,self).__init__(**kwargs)
        box1 = BoxLayout(orientation='vertical')
        btn1 = Button(text='go to other')
        btn1.bind(on_press=self.changer)
        for i in 1000:
            btn = Button(text=str('A button #', i))
            box1.add_widget(btn)
    def changer(self, *args):
        self.manager.current = 'other'


class OtherScreen(Screen):
    def __init__(slef, **kwargs):
        super(OtherScreen,self).__init__(**kwargs)
        float = FloatLayout()
        btn2 = Button(text='go to list')
        btn2.bind(on_press=self.changer)

    def changer(self, *args):
        self.manager.current = 'list'



sm = ScreenManager()
sm.add_widget(ListScreen(name='list'))
sm.add_widget(OtherScreen(name='other'))

class MusicApp(App):
    def build(self):

        Window.size = (480, 800)
        Window.fullscreen = False
        par = dirname(dirname(abspath(__file__)))
        return sm

if __name__ == '__main__':
    home = MusicApp()
    home.run()
