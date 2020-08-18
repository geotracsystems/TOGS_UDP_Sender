# setup.py is not currently being used
from setuptools import setup


setup(
    name="TOGS UDP Sender",
    version='',
    scripts=["togs_udp_sender.py"],
    author="Syed Raheem",
    author_email="syed_raheem@trimble.com",
    description="Test tool for sending various TOGS messages to the backend over UDP."
)
