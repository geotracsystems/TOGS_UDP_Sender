## Introduction
Test tool for sending various TOGS messages to the backend over UDP. 
Currently supports:
 * LMDirect (Calamp)
 * BEP (Bluetree).
 * UMF:
    * Dual Mode AVL
    * OOTN (Begin Timer, Back In Vehicle)

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
### Adding Message Formats
1. create a format_handler in the message folder:
```python
    def my_handler(args):
        ''' args is a namespace with every parameter from the command line or gui'''
        x = args.myfield
        ''' return a hex string of format "FF FF FF FF FF" '''
        return hex_str
```
In ```togs_udb_sender.py```:
1. add a new fancyname
    ```fancyname = 'This Message Format' ```
2. add your handler to ```message_format_handlers[fancyname]```
    ```python
    message_format_handlers = {
        ...
        fancyname: my_handler,
    }
    ```
3. add required fields for your message (ones used in ```my_handler()```)
```python
    message_format_fields = {
        ...
        fancyname: ['latitude', 'longitude', 'speed', 'event_id', 'seqno', 'myfield'],
    }
```
4. add any new fields you're using
```python
    field_descriptions = {
        ...
        'myfield': {
            'help': "Description of the field",
            'type': [str | int | etc.],
            'default': value,
        },
    }
```
