import tkinter as tk
import tkinter.simpledialog as sd
from playsound import playsound
import argparse
import subprocess
import re

parser = argparse.ArgumentParser(description='TTS Program for keyboard input.')
parser.add_argument('--default_tts', action='store_true', help='Enable the use of default TTS engine (Espeak)')
parser.add_argument('--arm', action='store_true', help='Specify if the processor is ARM for Piper.')
args = parser.parse_args()

IS_ARM = args.arm
USE_DEFAULT_TTS = args.default_tts
SPEECH_TEXT = ""
FONT_SIZE = 24
BAR_COLOR = '#0098fc'
STATUS_TEXT_COLOR_GO = '#1fff0f'
STATUS_TEXT_COLOR_STOP = '#ff2d0d'
TEXT_COLOR = 'white'
STATUS_TOGGLE = True

# Used to give context from text
mode_id = 0
modes = [
    "Write",
    "Math",
    "Chess"
]

# Define functions to increment or decrement the settings based on keyboard shortcuts
if USE_DEFAULT_TTS:
    import pyttsx3
    engine = pyttsx3.init()

    # Set the initial values for volume, rate, and voice
    volume = engine.getProperty('volume')
    rate = engine.getProperty('rate')
    voices = engine.getProperty('voices')
    voice_id = 11 # Default, (English)
    
    # Define a function to update the displayed settings
    def update_settings():
        volume_label.config(text=f" Volume: {int(volume * 100)}")
        rate_label.config(text=f"| Rate: {rate}")
        voice_label.config(text=f"| Voice: {(voices[voice_id].name).capitalize()}")
        mode_label.config(text=f'Mode: {modes[mode_id]}')

    def increment_volume(event):
        global volume
        volume += 0.1
        if volume > 1.0:
            volume = 1.0
        engine.setProperty('volume', volume)
        update_settings()

    def decrement_volume(event):
        global volume
        volume -= 0.1
        if volume < 0.0:
            volume = 0.0
        engine.setProperty('volume', volume)
        update_settings()

    def increment_volume(event):
        global volume
        volume += 0.1
        if volume > 1.0:
            volume = 1.0
        engine.setProperty('volume', volume)
        update_settings()

    def decrement_volume(event):
        global volume
        volume -= 0.1
        if volume < 0.0:
            volume = 0.0
        engine.setProperty('volume', volume)
        update_settings()

    def increment_rate(event):
        global rate
        rate += 10
        if rate > 500:
            rate = 500
        engine.setProperty('rate', rate)
        update_settings()

    def decrement_rate(event):
        global rate
        rate -= 10
        if rate < 0:
            rate = 0
        engine.setProperty('rate', rate)
        update_settings()

    def increment_voice(event):
        global voice_id
        voice_id += 1
        if voice_id >= len(voices):
            voice_id = 0
        engine.setProperty('voice', voices[voice_id].id)
        update_settings()

    def decrement_voice(event):
        global voice_id
        voice_id -= 1
        if voice_id < 0:
            voice_id = len(voices) - 1
        engine.setProperty('voice', voices[voice_id].id)
        update_settings()
    
    def increment_mode(event):
        global mode_id
        mode_id += 1
        if mode_id >= len(modes):
            mode_id = 0
        update_settings()

    # Define a function to display the help text
    def display_help():
        help_text = """Available commands:
        Ctrl + Q: Clear the text box
        Ctrl + A: Increase Volume
        Ctrl + Z: Decrease Volume
        Ctrl + S: Increase Speech rate
        Ctrl + X: Decrease Speech rate
        Ctrl + D: Increment Voice (forward)
        Ctrl + C: Decrement Voice (backward)
        Ctrl + M: Increment Mode
        Ctrl + P: Play All Text
        Ctrl + Backspace/Delete: Exit Program
        Ctrl + H: Display this help text"""
        sd.messagebox.showinfo("Help", help_text)

else:
    voice_id = 0
    voices = [
        ("Male", "en-us-ryan-high.onnx"),
        ("Female", "en-us-libritts-high.onnx")
    ]

    # Define a function to update the displayed settings
    def update_settings():
        voice_label.config(text=f"Voice: {voices[voice_id][0]}")
        mode_label.config(text=f'| Mode: {modes[mode_id]}')

    def increment_volume(event):
        pass

    def decrement_volume(event):
        pass

    def increment_rate(event):
        pass
    
    def decrement_rate(event):
        pass

    def increment_voice(event):
        global voice_id
        voice_id += 1
        if voice_id >= len(voices):
            voice_id = 0
        update_settings()

    def decrement_voice(event):
        global voice_id
        voice_id -= 1
        if voice_id < 0:
            voice_id = len(voices)-1
        update_settings()
    
    def increment_mode(event):
        global mode_id
        mode_id += 1
        if mode_id >= len(modes):
            mode_id = 0
        update_settings()

    # Define a function to display the help text
    def display_help():
        help_text = """Available commands:

    Ctrl + Q: Clear the text box
    Ctrl + D: Increment Voice (forward)
    Ctrl + C: Decrement Voice (backward)
    Ctrl + M: Increment Mode
    Ctrl + P: Play All Text
    Ctrl + Backspace/Delete: Exit Program
    Ctrl + H: Display this help text"""
        sd.messagebox.showinfo("Help", help_text)

def play_tts(text):
    global USE_DEFAULT_TTS
    toggle_status()

    text = re.sub(r'[^a-zA-Z0-9 ,.?!@$%&*~\-+=/]', '', text)
    if modes[mode_id] == "Chess":
        pass

    elif modes[mode_id] == "Math":
        text = text.replace(' % ', ' modulus ')
        text = text.replace('==', ' equals ')
        text = text.replace('~=', ' is not equal to ')
        text = text.replace('>=', ' is greater than or equal to ')
        text = text.replace('<=', ' is less than or equal to ')
        text = text.replace('=', ' equals ')
        text = text.replace('>', ' is greater than ')
        text = text.replace('<', ' is less than ')
        text = text.replace('+', ' plus ')
        text = text.replace('-', ' minus ')
        text = text.replace('*', ' times ')
        text = text.replace('/', ' divided by ')

        # Add more modes if desired

    if USE_DEFAULT_TTS:
        engine.say(text)
        engine.runAndWait()
    else:
        command = f"echo \'{text}\' | ./piper"
        if IS_ARM: command += "_arm"
        command += f"/piper -m voices/{voices[voice_id][1]} --output_file output.wav"
        print(command)
        subprocess.run(command, shell=True)
        playsound('output.wav')
    toggle_status()

def clear_text(event):
    text_box.delete(1.0, tk.END)

def exit_app(event):
    root.destroy()

def play_all_text(event):
    play_tts(text_box.get("1.0", "end-1c"))

def toggle_status():
    global STATUS_TOGGLE
    STATUS_TOGGLE = not STATUS_TOGGLE
    if STATUS_TOGGLE:
        status_label.config(fg=STATUS_TEXT_COLOR_GO, text=' GO')
    else:
        status_label.config(fg=STATUS_TEXT_COLOR_STOP, text=' STOP')
    settings_frame.update()

# Define a function to handle key presses
def on_key_press(event):
    global SPEECH_TEXT
    # Capture the text from the key press and add it to the text box
    if not (event.state & 0x4):
        if event.keysym == 'BackSpace':
            SPEECH_TEXT = SPEECH_TEXT[:-1] # Remove the last character from SPEECH_TEXT
        else:
            text = event.char
            print("Key pressed:", text)
            SPEECH_TEXT += text

            if text in [",", ".", "?", "!"]:
                play_tts(SPEECH_TEXT)
                SPEECH_TEXT = ''

# Create the main window, and initialize sound
root = tk.Tk()

# Create the text box
text_box = tk.Text(root, font=('Helvetica', FONT_SIZE, 'normal'))
text_box.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
text_box.focus()

# Create the frame for the settings
settings_frame = tk.Frame(root)
settings_frame.config(bg=BAR_COLOR)
settings_frame.pack(side=tk.BOTTOM, fill=tk.X)

# Create the labels for the settings
volume_label = tk.Label(settings_frame, bg=BAR_COLOR, fg=TEXT_COLOR, text=f"", font=('Helvetica', 16, 'normal'))
rate_label = tk.Label(settings_frame, bg=BAR_COLOR,fg=TEXT_COLOR, text=f"", font=('Helvetica', 16, 'normal'))
voice_label = tk.Label(settings_frame, bg=BAR_COLOR, fg=TEXT_COLOR, text=f"", font=('Helvetica', 16, 'normal'))
mode_label = tk.Label(settings_frame, bg=BAR_COLOR,fg=TEXT_COLOR, text=f"", font=('Helvetica', 16, 'normal'))
status_label = tk.Label(settings_frame, bg=BAR_COLOR,fg=STATUS_TEXT_COLOR_STOP, text=f"", font=('Helvetica', 16, 'normal'))
help_label = tk.Label(settings_frame, bg=BAR_COLOR,fg=TEXT_COLOR, text="Ctrl + H to display actions ", font=('Helvetica', 16, 'normal'))

update_settings()
toggle_status()

# Pack the labels into the settings frame
volume_label.pack(side=tk.LEFT)
rate_label.pack(side=tk.LEFT)
voice_label.pack(side=tk.LEFT)
mode_label.pack(side=tk.LEFT)
status_label.pack(side=tk.LEFT)
help_label.pack(side=tk.RIGHT)

# Bind the keyboard shortcuts for the settings
root.bind("<Control-KeyPress-a>", increment_volume)
root.bind("<Control-KeyPress-z>", decrement_volume)
root.bind("<Control-KeyPress-s>", increment_rate)
root.bind("<Control-KeyPress-x>", decrement_rate)
root.bind("<Control-KeyPress-d>", increment_voice)
root.bind("<Control-KeyPress-c>", decrement_voice)
root.bind("<Control-KeyPress-m>", increment_mode)
root.bind("<Control-KeyPress-p>", play_all_text)
root.bind("<Control-KeyPress-q>", clear_text)
root.bind("<Control-h>", lambda event: display_help())
root.bind("<Control-BackSpace>", exit_app)
root.bind("<Control-Delete>", exit_app)


# Bind the key press event to the text box
text_box.bind("<Key>", on_key_press)

# Set window attributes
root.title("Text to Speech")
root.attributes('-fullscreen', True)
# root.overrideredirect(True)

root.mainloop()