import kivy
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.carousel import Carousel
from kivy.uix.image import AsyncImage

# kivy.require('1.0.6')  # replace with your current kivy version !

from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.label import Label


class GalleryApp(App):
    def build(self):
        carousel = Carousel(direction='right')
        for i in range(10):
            src = "DCIM\Design.png"
            image = AsyncImage(source=src, allow_stretch=True)
            carousel.add_widget(image)
        return carousel
        #return BoxLayout()


def main():
    home = GalleryApp()
    home.run()


if  __name__ =='__main__':main()

