import os
from Canvas import Rectangle

from kivy.core.window import Window
from kivy.graphics.instructions import Canvas
from kivy.uix.boxlayout import BoxLayout

from kivy.core.audio import SoundLoader

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
    path = '/RaspberryPiPhone/songs'
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




class MusicApp(App):
    def build(self):

        Window.size = (480, 800)
        Window.fullscreen = False
        par = dirname(dirname(abspath(__file__)))
        return FloatLayout()

if __name__ == '__main__':
    home = MusicApp()
    home.run()
