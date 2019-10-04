## Introduction
Test tool for sending various TOGS messages to the backend over UDP. Currently supports LMDirect (Calamp) and BEP (Bluetree) protocols.

Executable files for Windows (.exe) can be found in the `dist/` directory. There's no need to install Python for running this tool in GUI mode.
However for running the tool in CLI mode, Python and some pre-requisites are required. See Developer Notes section for more details.

## Usage
### GUI Usage
Simply double click the .exe file in `dist/`. The instructions on the screen are intuitive.
To send a single message, select the "single" tab. The "csv" tab allows you to send multiple messages in a CSV.

### CLI Usage
CLI Usage is meant for advanced users or to run long running scripts from CI system for testing. Python needs to be 

Single Mode:

`python togs_udp_sender.py --ignore-gooey single <modem> <host> <port> <esn> <latitude> <longitude> <speed> <eventid>`

CSV Mode:
`python togs_udp_sender.py --ignore-gooey csv <filename>`


**Resources**
https://docs.google.com/document/d/1qkBsVFaa77FN0-WFOiDpIv2s2DolV7_SGqaZF5kQ6tg/edit?usp=sharing


## Developer Notes 
### Prerequisites for running with Python or development
This tool works with Python 3.7 or higher.
The following packages need to be installed using `pip`:
```
pip install Gooey
pip install PyInstaller
```

To create executable, we are using PyInstaller with the following options.
```
pyinstaller -F --windowed togs_udp_sender.py
```
