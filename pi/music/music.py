import os
from Canvas import Rectangle

from kivy.core.window import Window
from kivy.graphics.instructions import Canvas
from kivy.uix.boxlayout import BoxLayout

from kivy.core.audio import SoundLoader
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.scrollview import ScrollView
from kivy.uix.slider import Slider

from kivy.app import App
from kivy.app import runTouchApp
from os.path import dirname, abspath
from kivy.uix.label import Label

from kivy.uix.floatlayout import FloatLayout



class Sound():
    playing = False
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
        playing = True
    def pause(self):
        sound.stop()
        playing = False
    def playAtTime(self, time):
        if playing == False:
            play()
        sound.seek(time)

    def next(self):
        sound.unload()
        Songsplayed = Songsplayed + 1
        if Songsplayed > count - 1:
            sound = first
            Songsplayed = 0
        else:
            sound = SoundLoader.load(d.get(Songsplayed))
        if playing:
            play()


    def back(self):
        sound.unload()
        if (Songsplayed-1)%(count-1) == 0:
            sound = SoundLoader.load(d.get(count - 1))
        else:
            sound = SoundLoader.load(d.get((Songsplayed-1)%(count-1)))
        if playing:
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
    def __init__(self, **kwargs):
        super(OtherScreen,self).__init__(**kwargs)
        float = FloatLayout()
        label = Label(text='0.00')
        s = Slider(min = 0, max = sound.length, value = 0)
        btn2 = Button(text='go to list')
        btn2.bind(on_press=self.changer)
        s.bind(value=self.sliderProgress)
        float.add_widget(btn2)
        float.add_widget(s)

    def changer(self, *args):
        self.manager.current = 'list'

    def sliderProgress(self, value):
        label.text = str(value)


sm = ScreenManager()
sm.add_widget(ListScreen(name='list'))
sm.add_widget(OtherScreen(name='other'))

class MusicApp(App):
    def build(self):

        Window.size = (480, 800)
        Window.fullscreen = False
        par = dirname(dirname(abspath(__file__)))
        root = ScrollView(size_hint=(1, None), size=(Window.width,
            Window.height))
        root.add_widget(layout)
        runTouchApp(root)
        return sm

if __name__ == '__main__':
    home = MusicApp()
    home.run()
