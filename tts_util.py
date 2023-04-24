import datetime
import os

def decimal_to_integer(number):
    return int(str(number).split('.')[1])

def delete_old_wav_files(DAYS_TO_KEEP): # Remove them if older than X weeks
    export_audio_dir = os.path.join(os.getcwd(), 'export_audio')

    if DAYS_TO_KEEP <= 0: # If invalid, delete all
        for file_name in os.listdir(export_audio_dir):
            if file_name.endswith('.wav'):
                file_path = os.path.join(export_audio_dir, file_name)
                os.remove(file_path)
    else:
        normal_days_keep = datetime.datetime.now() - datetime.timedelta(days=DAYS_TO_KEEP)

        for file_name in os.listdir(export_audio_dir):
            if file_name.endswith('.wav'):               
                file_path = os.path.join(export_audio_dir, file_name)
                file_modified_time = datetime.datetime.fromtimestamp(os.path.getmtime(file_path))
                if file_modified_time < normal_days_keep:
                    os.remove(file_path)

def delete_old_text_files(DAYS_TO_KEEP): # Remove them if older than X weeks
    export_text_dir = os.path.join(os.getcwd(), 'export_text')
    if DAYS_TO_KEEP <= 0: # If invalid, delete all
        for file_name in os.listdir(export_text_dir):
            if file_name.endswith('.txt'):
                file_path = os.path.join(export_text_dir, file_name)
                os.remove(file_path)
    else:
        normal_days_keep = datetime.datetime.now() - datetime.timedelta(days=DAYS_TO_KEEP)

        for file_name in os.listdir(export_text_dir):
            if file_name.endswith('.txt'):  
                file_path = os.path.join(export_text_dir, file_name)
                file_modified_time = datetime.datetime.fromtimestamp(os.path.getmtime(file_path))
                if file_modified_time < normal_days_keep:
                    os.remove(file_path)

def create_dirs():
    if not os.path.exists('export_audio'):
        os.makedirs('export_audio')

    if not os.path.exists('export_text'):
        os.makedirs('export_text')

def initialize_voices():
    if not os.path.exists('voices'):
        print("Error: \'voices\' could not be found.\nYou do not have any voices installed.\nMake sure to follow the installation instructions or use \'--default_tts\' if you have Espeak installed.")
        exit(0)

    with open("voices/avaliable_voices.txt", "r") as f:
        lines = f.readlines()
    
    voices = [tuple(line.strip().split(":")) for line in lines]

    return voices
