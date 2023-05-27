## Speech To Text Telegram bot
- Uses voice and audio messages to translate them into text.
- Currently doesn't work with normal voice
- Partially works with abnormal voice
- Can be hosted and used by just launch (you need Telegram API key)

## Technical info
- Currently works with CPU and CUDA
- Supports documents of WAV format
- Supports Russian voice messages

## TODO
- Add support for video documents
- Add support for short video messages

## Libraries

- torch
- torchaudio
- librosa
- numpy 
- telebot
- soundfile

## How to install (for Windows)

If you want to run this bot:
For torch and torchaudio:
https://pytorch.org/ install packages from there

Other packages can be installed using "pip install"

## How to install (for Ubuntu/Linux)

Install torch and torchaudio from https://pytorch.org/

Install libsndfile1 from "lunar" repository

Example:

```sudo add-apt-repository 'deb http://cz.archive.ubuntu.com/ubuntu lunar main'```

```sudo apt-get install libsndfile1```

https://packages.ubuntu.com/lunar/libsndfile1


Other packages can be installed normally via "pip install"

## How to launch

- Add file key.txt to your program's root folder (where main.py stored)
- Fill it with telegram bot API key
- Run telegram bot just by launching main.py file via console (python main.py) or by your IDE.
