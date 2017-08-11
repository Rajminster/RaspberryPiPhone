from os.path import abspath, dirname

from Canvas import Rectangle

from kivy.app import App, runTouchApp
from kivy.clock import mainthread
from kivy.core.window import Window
from kivy.core.audio import SoundLoader
from kivy.graphics.instructions import Canvas, Image
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.progressbar import ProgressBar
from kivy.uix.screenmanager import Screen, ScreenManager, CardTransition
from kivy.uix.scrollview import ScrollView
from kivy.uix.slider import Slider

import os

################################################################################
#           TODO: if a song is selected, correctly update song_number          #
################################################################################
class Music_Player():
    """Class to play songs from the /Songs directory

    Attribute:
        PATH (str): path to wherever the songs are saved
    """

    def __init__(self):
        """Constructor which sets class-wide variables and loads the library"""
        self.playing = False
        self.song_number = 0 # index of which song played most recently
        self.PATH = 'Songs'
        self.library = []
        i = 0
        for file_name in os.listdir(self.PATH):
            self.library.append(file_name)
            i += 1
        self.current_playing = SoundLoader.load(self.library[0])

    def play(self):
        """Play the song which is labeled as current_playing"""
        if self.current_playing:
            self.current_playing.play()
            self.playing = True
        else:
            ####################################################################
            #          TODO: write a try except block to handle this           #
            ####################################################################
            raise TypeError('Song selected is None')

    def pause(self):
        """Pause any playing song"""
        self.current_playing.stop()
        self.playing = False

    def playAtTime(self, time):
        """Start playing a song at a given time"""
        if not self.current_playing:
            self.play()
        self.current_playing.seek(time)

    def next(self):
        """Play the next song listed in the library"""
        self.current_playing.unload()
        self.song_number += 1
        self.current_playing = SoundLoader.load(self.library[self.song_number % len(library)])
        if self.playing:
            self.play()

    def back(self):
        """Play the previously listed song"""
        self.current_playing.unload()
        self.song_number -= 1
        self.current_playing = SoundLoader.load(self.library[self.song_number % len(library)])
        if self.playing:
            self.play()

class ListScreen(Screen):
    def __init__(self, **kwargs):
        super(ListScreen,self).__init__(**kwargs)
        self.on_enter()

    def changer(self, *args):
        self.parent.current = 'other'

    @mainthread
    def on_enter(self):
        layout = self.ids.listlayout
        box1 = BoxLayout(orientation='vertical')
        btn1 = Button(text='go to other')
        btn1.bind(on_press=self.changer)
        for i in range(10):
            btn = Button(text=str('A button #'), size_hint = (None,None), on_press = self.changer)
            box1.add_widget(btn)
        root = ScrollView(size_hint=(1, None), size=(Window.width, Window.height))
        root.add_widget(box1)
        layout.add_widget(root)
        print 'Test'

class OtherScreen(Screen):
    def __init__(self, **kwargs):
        super(OtherScreen,self).__init__(**kwargs)
        self.on_enter()

    def changer(self, *args):
        self.parent.current = 'list'

    def sliderProgress(self, value):
        self.label.text = str(value)

    @mainthread
    def on_enter(self):
        layout = self.ids.otherlayout
        float = FloatLayout()
        player = Music_Player()
        self.label = Label(text='0.00')
        s = Slider(min=0, max=player.current_playing.length, value=0, value_track=True, value_track_color=[1, 0, 0, 1])
        s.step = .01
        btnp = Button(text='play')
        btnpau = Button(text='pause')
        btnb = Button(text='back')
        btn2 = Button(text='go to list')
        btnn = Button(text='next')
        pb = ProgressBar(max=player.current_playing.length)
        # pb.bind(value=self.sliderProgress \
        # (player \
        # .current_playing. \
        # get_pos()))
        # btn2.bind(on_press=self.changer)
        # btnp.bind(on_press=player.play())
        # btnpau.bind(on_press=player.pause())
        # btnb.bind(on_press=player.back())
        # btnn.bind(on_press=player.next())
        # s.bind(value=self.sliderProgress)
        # s.bind(on_touch_up=player.playAtTime(value))
        float.add_widget(btn2)
        float.add_widget(s)
        layout.add_widget(float)

class ScreenManagement(ScreenManager):
    ScreenManager.transition =  CardTransition()
    pass

class MusicApp(App):
    def build(self):
        Window.size = (480, 800)
        Window.fullscreen = False
        return ScreenManagement()

if __name__ == '__main__':
    home = MusicApp()
    home.run()
