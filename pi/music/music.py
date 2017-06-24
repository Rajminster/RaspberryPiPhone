from kivy.core.audio import SoundLoader

# need to define clicked in UI

sound = SoundLoader.load(clicked)

if sound:
    sound.play()
