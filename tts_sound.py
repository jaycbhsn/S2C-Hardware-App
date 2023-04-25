import pygame
import keyboard
import os

def play_audio(filename, volume, rate):
    print(f"Playing sounds with these settings: Volume: {volume}, Rate: {rate:.1f}")

    # Initialize pygame mixer
    pygame.mixer.init()

    if int(rate) != 1:
        change_rate(filename, rate)

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

def change_rate(filename, rate):
    output_filename = 'export_audio/audio.wav'
    # Check if the file exists
    if not os.path.isfile(filename):
        print(f"File '{filename}' does not exist.")
        return
    
    # Use ffmpeg to change the audio speed
    os.system('ffmpeg -i "{}" -filter:a "atempo={}" -codec:a pcm_s16le -ar 44100 -ac 2 "{}"'.format(filename, rate, output_filename))
    
    # Overwrite the original file with the processed audio
    os.replace(output_filename, filename)
