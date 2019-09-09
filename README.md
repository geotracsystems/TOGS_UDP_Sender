Test tool for sending various TOGS messages to the backend over UDP. Currently supports LMDirect (Calamp) and BEP (Bluetree) protocols.

**Usage**

Send file:

`python3 test_bluetree_msg.py <imei> <host> <port> <filename>`

Send single message:

`python3 test_bluetree_msg.py <imei> <host> <port> single <latitude> <longitude> <speed> <eventid>`


**Resources**
https://docs.google.com/document/d/1qkBsVFaa77FN0-WFOiDpIv2s2DolV7_SGqaZF5kQ6tg/edit?usp=sharing
