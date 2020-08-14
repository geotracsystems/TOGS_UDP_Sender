from setuptools import setup


def get_version():
    f = open('togs_udp_sender.spec')
    for line in f.read().splitlines():
        if line.startswith('__version__'):
            delim = "'"
            return line.split(delim)[1]
        else:
            raise RuntimeError("Unable to find version string.")


setup(
    name="TOGS UDP Sender",
    version=get_version(),
    scripts=["togs_udp_sender.py"],
    author="Syed Raheem",
    author_email="syed_raheem@trimble.com",
    description="Test tool for sending various TOGS messages to the backend over UDP."
)
