import logging
import sys


def logger(module):
    # Create a custom logger
    log = logging.getLogger(module)
    log.setLevel(logging.DEBUG)

    # Create handlers
    c_handler = logging.StreamHandler(stream=sys.stdout)
    f_handler = logging.FileHandler('log.txt')
    # f_handler.setLevel(logging.DEBUG)

    # Create formatters and add it to handlers
    c_format = logging.Formatter('%(levelname)s - %(message)s')
    f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    c_handler.setFormatter(c_format)
    f_handler.setFormatter(f_format)

    # Add handlers to the logger
    log.addHandler(c_handler)
    log.addHandler(f_handler)

    return log
