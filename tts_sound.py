import pygame
import keyboard

def play_audio(filename, volume, rate):
    print(f"Playing sounds with these settings: Volume: {volume}, Rate: {rate:.1f}")

    # Initialize pygame mixer
    pygame.mixer.init()

    # Load the audio data and set volume
    sound = pygame.mixer.Sound(filename)
    sound.set_volume(volume)
    channel = sound.play()

    # define the callback function for keypresses
    def stop_sound(event):
        if event.name == "ctrl":
            # stop the sound
            channel.stop()
            # unregister the callback function
            keyboard.unhook(stop_sound)

    # register the callback function for keypressesrate
    keyboard.hook(stop_sound)

    # wait while the sound is playing
    while channel.get_busy():
        pass
    
    pygame.mixer.quit()
