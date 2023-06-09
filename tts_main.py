import tkinter.simpledialog as sd
import tkinter as tk
import subprocess
import datetime
import argparse
import re
import os

import tts_sound
import tts_util

parser = argparse.ArgumentParser(description='TTS Program for keyboard input.')
parser.add_argument('--default_tts', action='store_true', help='Enable the use of default TTS engine (Espeak)')
parser.add_argument('--arm', action='store_true', help='Specify if the processor is ARM for Piper.')
parser.add_argument('--forget_audio', action='store_true', help='Conserve storage by not saving audio beyond the most reccent call.')
args = parser.parse_args()

USE_DEFAULT_TTS = args.default_tts
IS_ARM = args.arm
FORGET_AUDIO = args.forget_audio

FONT_SIZE = 24
TEXT_PADDING = 4
MAX_RATE = 2.0
MIN_RATE = 0.5
BAR_COLOR = '#0098fc'
STATUS_TEXT_COLOR_GO = '#1fff0f'
STATUS_TEXT_COLOR_STOP = '#ff0008'
TEXT_BACKGROUND_COLOR = 'white'
STATUS_TOGGLE = False
DAYS_TO_KEEP = 3

# Used to give context from text
mode_id = 0
modes = [
    "Write",
    "Math",
    "Chess"
]

tts_util.create_dirs()

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
        rate_label.config(text=f"| Rate: x{rate}")
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
        Ctrl + O: Export Text
        Ctrl + Backspace/Delete: Exit Program
        Ctrl + H: Display this help text"""
        sd.messagebox.showinfo("Help", help_text)

else:
    volume = 1.0
    rate = 1.0
    voice_id = 0
    voices = tts_util.initialize_voices()
    
    # Define a function to update the displayed settings
    def update_settings():
        volume_label.config(text=f" Volume: {int(volume * 100)}")
        rate_label.config(text=f"| Rate: x{rate:.1f}")
        voice_label.config(text=f"| Voice: {voices[voice_id][0]}")
        mode_label.config(text=f'| Mode: {modes[mode_id]}')

    def increment_volume(event):
        global volume
        volume += 0.1
        if volume > 1.0:
            volume = 1.0
        update_settings()

    def decrement_volume(event):
        global volume
        volume -= 0.1
        if volume < 0.0:
            volume = 0.0
        update_settings()

    def increment_rate(event):
        global rate
        rate += 0.1
        if rate > MAX_RATE:
            rate = MAX_RATE
        update_settings()

    def decrement_rate(event):
        global rate
        rate -= 0.1
        if rate < MIN_RATE:
            rate = MIN_RATE
        update_settings()

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
    Ctrl + L: Play Current Line
    Ctrl + O: Export Text
    Ctrl + Backspace/Delete: Exit Program
    Ctrl + H: Display this help text"""
        sd.messagebox.showinfo("Help", help_text)

def play_tts(text, isFull):
    global USE_DEFAULT_TTS
    toggle_speech_status()
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
        toggle_speech_status()
    else:
        global volume, rate

        audio = "export_audio/" 
        audio += "FULL_" if isFull else ""
        audio += datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S_audio.wav") if not FORGET_AUDIO else "audio.wav"
        
        command = f"echo \'{text}\' | ./piper" 
        command += "_arm" if IS_ARM else ""
        command += f"/piper -m voices/{voices[voice_id][1]} --output_file " + audio
        print("Command: ", command, "\nSaved Audio as ", audio)
        subprocess.run(command, shell=True)
        tts_sound.play_audio(audio, volume, rate)
        toggle_speech_status()

def clear_text(event):
    text_box.delete(1.0, tk.END)

def exit_app(event):
    root.destroy()

def play_line(event):
    index = text_box.index(tk.INSERT)
    line_start = text_box.index(f"{index} linestart")
    line_end = text_box.index(f"{index} lineend")
    current_line = text_box.get(line_start, line_end)
    play_tts(current_line, False)
    print("Line spoken: ", current_line)

def play_all_text(event):
    play_tts(text_box.get("1.0", "end-1c"), True)

def export_text(event):
    text = text_box.get("1.0", "end-1c")
    # Currently not done...
    # if not tts_util.write_to_usb(text)):
    with open(datetime.datetime.now().strftime("export_text/%Y-%m-%d_%H:%M:%S_text.txt"), "w") as f:
        f.write(text)
    f.close()

# Define a function to handle key presses
def on_key_press(event):
    # Capture the text from the key press and add it to the text box
    if not (event.state & 0x4): # If control is not being pressed

        # Auto complete word? TBD if should be added
        if event.char == '\t':
            pass
        else:
            if event.char in [",", ".", "?", "!", ";"]: # Play audio if termination of line character found
                play_line(event)

# Defines if the app is currently speaking
def toggle_speech_status():
    global STATUS_TOGGLE
    STATUS_TOGGLE = not STATUS_TOGGLE
    if STATUS_TOGGLE:
        status_label.config(fg=STATUS_TEXT_COLOR_GO, text=' GO')
    else:
        status_label.config(fg=STATUS_TEXT_COLOR_STOP, text=' CTRL TO STOP')
    settings_frame.update()

# Sets character behind the cursor to a specified color
def set_last_char_color():
    text_box.tag_remove("last_char_color", "1.0", tk.END)
    text_box.tag_add("last_char_color", "insert-1c", "insert")
    text_box.after(70, set_last_char_color)

# Create the main window, and initialize sound
root = tk.Tk()

# Create the text box
text_box = tk.Text(root, font=('Helvetica', FONT_SIZE, 'normal'))
text_box.tag_config("last_char_color", foreground='#ff0008') # set color for the tag
text_box.grid(row=0, column=0, sticky='nsew')
text_box.focus()
text_box.lower()

# Create the frame for the settings
settings_frame = tk.Frame(root)
settings_frame.config(bg=BAR_COLOR, width=root.winfo_screenwidth(), height=30)
settings_frame.grid(row=1, column=0, sticky='ew')

root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

# Create the labels for the settings
volume_label = tk.Label(settings_frame, pady=TEXT_PADDING, bg=BAR_COLOR, fg=TEXT_BACKGROUND_COLOR, text=f"", font=('Helvetica', 16, 'normal'))
rate_label = tk.Label(settings_frame, pady=TEXT_PADDING, bg=BAR_COLOR,fg=TEXT_BACKGROUND_COLOR, text=f"", font=('Helvetica', 16, 'normal'))
voice_label = tk.Label(settings_frame, pady=TEXT_PADDING, bg=BAR_COLOR, fg=TEXT_BACKGROUND_COLOR, text=f"", font=('Helvetica', 16, 'normal'))
mode_label = tk.Label(settings_frame, pady=TEXT_PADDING, bg=BAR_COLOR,fg=TEXT_BACKGROUND_COLOR, text=f"", font=('Helvetica', 16, 'normal'))
status_label = tk.Label(settings_frame, pady=TEXT_PADDING, bg=BAR_COLOR,fg=STATUS_TEXT_COLOR_STOP, text=f"", font=('Helvetica', 16, 'normal'))
help_label = tk.Label(settings_frame, pady=TEXT_PADDING, bg=BAR_COLOR,fg=TEXT_BACKGROUND_COLOR, text="Ctrl + H to display actions ", font=('Helvetica', 16, 'normal'))

update_settings()
toggle_speech_status()
set_last_char_color() # initialize the loop

tts_util.delete_old_wav_files(DAYS_TO_KEEP)
tts_util.delete_old_text_files(DAYS_TO_KEEP)

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
root.bind("<Control-KeyPress-l>", play_line)
root.bind("<Control-KeyPress-q>", clear_text)
root.bind("<Control-KeyPress-o>", export_text)
root.bind("<Control-KeyPress-h>", lambda event: display_help())
root.bind("<Control-BackSpace>", exit_app)
root.bind("<Control-Delete>", exit_app)

# Bind the key press event to the text box
text_box.bind("<Key>", on_key_press)

# Set window attributes
root.title("Text to Speech")
root.attributes('-topmost', 1)
root.attributes('-fullscreen', True)

# Move the labels to the top
settings_frame.lift()
volume_label.lift()
rate_label.lift()
voice_label.lift()
mode_label.lift()
status_label.lift()
help_label.lift()

root.mainloop()
