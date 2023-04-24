# S2C Hardware App

A Text to Speech app which runs on Linux x86 and ARM systems (such as Raspberry Pi).

![TTSAPP](https://user-images.githubusercontent.com/101217869/233815513-575ebfd4-f8be-4492-b853-67456042255b.gif)

**Author: Jacob Hansen**

_TTS Engine provided by Piper: https://github.com/rhasspy/piper_

## Installation:

First, install the required packages with pip, and run this on Python 3.7 or later **AS ROOT/with sudo** (This was built on Python 3.10):
```
wget https://github.com/jaycbhsn/S2C-Hardware-App/raw/main/requirements.txt
pip install -r requirements.txt
```

Once the requirements are installed, hollow the instructions for the most up to date release or an older release if you prefer:

[Current Release](https://github.com/jaycbhsn/S2C-Hardware-App/releases/latest)


_If you choose to use a different TTS engine such as Espeak (not recommended), use the flag '--default_tts' and install espeak on your OS with:_
```
apt-get install espeak -y
```
