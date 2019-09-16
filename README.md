Test tool for sending various TOGS messages to the backend over UDP. Currently supports LMDirect (Calamp) and BEP (Bluetree) protocols.

Executable files for Windows (.exe) can be found in the `dist/` directory. There's no need to install Python for running this tool.

**Usage**

Send file:

`test_bluetree_msg.exe <imei> <host> <port> <filename>`

Send single message:

`test_bluetree_msg.exe <imei> <host> <port> single <latitude> <longitude> <speed> <eventid>`


**Resources**
https://docs.google.com/document/d/1qkBsVFaa77FN0-WFOiDpIv2s2DolV7_SGqaZF5kQ6tg/edit?usp=sharing


**Developer Note** 

To create executable, we are using PyInstaller.
```
pyinstaller -F test_lmdirect_msg.py
pyinstaller -F test_bluetree_msg.py
```
