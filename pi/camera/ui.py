from kivy.uix.button import Button as b
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.gesture import Gesture, GestureDatabase
from kivy.lang import Builder
from camera.py import Camera

# builds a camera

cmra = Camera()


# builds the screens using Builder and screenmanager as a pseudo-kv file

Builder.load_string("""
<CameraScreen>:
    on_enter: cmra
    AnchorLayout:

        anchor_x:
        anchor_y:

        Button:
            border: Line(circle=150, 150, 50)
            close: True
            on_press: cmra.image()
        Button:
            text: 'Low Light'
            on_press: cmra.lowLightImage()

        Button:
            text: 'record'
            on_press: root.manager.current = 'record'
<RecordScreen>
    BoxLayout:
        Button:
            border: Line(circle=150, 150, 50)
            close: True
            on_press: cmra.record()

        Button:
            text: 'capture image'
            on_press: root.manager.current = 'camera'
""")

# class for the camera screen
# not exactly sure what this is actually for, but kivy documentation had it, so I have it

class CameraScreen(Screen):
    pass

# class for the Record screen ^

class RecordScreen(Screen):
    pass


# screen manager object that has both screens as widgets

sm = ScreenManager()
sm.add_widget(CameraScreen(name='camera'))
sm.add_widget(RecordScreen(name='record'))












class UI(App):
    # circle = ObjectProperty(None)
    # def __init__(self):
    #     I_button = b(text='Picture', font_size=12)
    #     I_button.border = Line(circle=150, 150, 50)
    #     V_button = b(text='Video', font_size=12)
    #     V_button.border = Line(circle=150, 150, 50)
    #     T_button = b(text='Timelapse', font_size=12)
    #     T_button.border = Line(circle=150, 150, 50)
    #     F_button = b(text='Flash', font_size=12)
    #
    #
    # def capture_image():
    #     self.image()
    #
    # # def capture_video():
    # #     self.record()
    #
    # def Screen_switch():
    #     self.switch()
    #
    # def run():
    #     while ui.is_open:
    #     I_button.bind(on_release=capture_image())
    #     V_button.bind(on_release=self.record())
    #     T_button.bind(on_release=self.timelapse())
    #     F_button.bind(on_release=self.flash())

    def build(self):
        return sm

    if __name__ == '__main__' :
        UI().run()
