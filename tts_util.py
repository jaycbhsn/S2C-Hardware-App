import datetime
import pyudev
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

def write_to_usb(text):
    # Create a pyudev context
    context = pyudev.Context()

    # Loop through all the USB devices
    for device in context.list_devices(subsystem='block', ID_BUS='usb'):
        # Check if the device is a storage device
        print(str(device))
        if device.get('ID_TYPE') == 'disk':
            # Get the path of the device
            device_path = os.path.join('/dev', device.get('DEVNAME'))
            # print("DEVICE PATH: ", device_path)
            # Create the path to the text file on the device
            filename = datetime.datetime.now().strftime("/sda1/%Y-%m-%d_%H-%M-%S_text.txt")
            text_file_path = device_path + filename
            # Write the content to the text file
            with open(text_file_path, 'w') as f:
                f.write(text)
            print(f"tts_util: File written to {text_file_path}")
            return True
    return False

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

