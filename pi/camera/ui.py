from kivy.uix.button import Button as b
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from camera.py import Camera

cmra = Camera()


Builder.load_string("""
<CameraScreen>:
    on_enter: cmra
    AnchorLayout:

        Button:
            border: Line(circle=150, 150, 50)
            close: True
            on_press: cmra.image()
        Button:
            text: 'Low Light'
            on_press: cmra.lowLightImage()
<RecordScreen>
    BoxLayout:
        Button:
            border: Line(circle=150, 150, 50)
            on_press: cmra.record()
""")






sm = ScreenManager()
sm.add












class UI():
    # circle = ObjectProperty(None)
    def __init__(self):
        I_button = b(text='Picture', font_size=12)
        I_button.border = Line(circle=150, 150, 50)
        V_button = b(text='Video', font_size=12)
        V_button.border = Line(circle=150, 150, 50)
        T_button = b(text='Timelapse', font_size=12)
        T_button.border = Line(circle=150, 150, 50)
        F_button = b(text='Flash', font_size=12)


    def capture_image():
        self.image()

    # def capture_video():
    #     self.record()

    def Screen_switch():
        self.switch()

    def run():
        while ui.is_open:
        I_button.bind(on_release=capture_image())
        V_button.bind(on_release=self.record())
        T_button.bind(on_release=self.timelapse())
        F_button.bind(on_release=self.flash())
