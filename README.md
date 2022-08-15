# KakaduFM
<img align="right" src="https://github.com/morgor/KakaduFM/raw/main/screenshot2.png" alt="KakaduFM screenshot">

Another player for internet radio stations, using the database https://www.radio-browser.info/.

Requirements:
- Windows 10 (tested)
- Python 3.10+ https://www.python.org/downloads/

Installation:
- download and unpack https://github.com/morgor/KakaduFM/archive/refs/heads/main.zip
- run treminal/console (cmd.exe or Power Shell)
- go to directory (use 'cd' command) 'main' (You can rename it)

<h2>Option 1 (global)</h2>

Download dependences:

    pip install -r requirements.txt

Running:

    python main.py

<h2>Option 2 (venv)</h2>

Download dependences:

    python -m venv venv
    venv\Scripts\activate.bat
    pip install -r requirements.txt

Running:

    venv\Scripts\activate.bat
    python main.py
