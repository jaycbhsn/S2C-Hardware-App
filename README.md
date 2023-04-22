# S2C Hardware App

A Text to Speech app which runs on Linux x86 and ARM systems (such as Raspberry Pi).

TTS Engine provided by Piper: https://github.com/rhasspy/piper

INSTALLATION:
First, install the required packages in pip, and run this on Python 3.7 or later (This was built on Python 3.10):
```
wget https://github.com/jaycbhsn/S2C-Hardware-App/raw/main/requirements.txt
pip install -r requirements.txt
```

Once the requirements are installed, hollow the instructions for the most up to date release or an older release if you prefer:

[Current Release](https://github.com/jaycbhsn/S2C-Hardware-App/releases/latest)


If you choose to use a different TTS engine such as Espeak (not recommended), use the flag '--default_tts' and install espeak on your OS with:
```
apt-get install espeak -y
```
