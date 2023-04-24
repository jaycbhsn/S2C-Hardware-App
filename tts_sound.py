from pygame import mixer
import keyboard

def play_audio(filename):
    # load the sound file and play it
    sound = mixer.Sound(filename)
    channel = sound.play()

    # define the callback function for keypresses
    def stop_sound(event):
        if event.name == "ctrl":
            # stop the sound
            channel.stop()
            # unregister the callback function
            keyboard.unhook(stop_sound)

    # register the callback function for keypresses
    keyboard.hook(stop_sound)

    # wait while the sound is playing
    while channel.get_busy():
        pass
