# S2C-Hardware-App

A Text to Speech app which runs on Linux x86 and ARM systems (such as Raspberry Pi).

TTS Engine provided by Piper: https://github.com/rhasspy/piper

INSTALLATION:
First, install the required packages in pip, and run this on Python 3.7 or later (This was built on Python 3.10):
```
wget 
pip install -r requirements.txt
```

Once the requirements are installed


If you choose to use a different TTS engine such as Espeak (not recommended), use the flag '--default_tts' and install espeak with:
```
sudo apt-get install espeak
pip install pyttsx3
```
