from dotenv import load_dotenv
import os
import logging

load_dotenv()


def get_key(key: str) -> str:
    value = os.getenv(key)
    return value


def logger_setup(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    c_handler = logging.StreamHandler()
    f_handler = logging.FileHandler('app/app.log')
    c_handler.setLevel(logging.INFO)
    f_handler.setLevel(logging.INFO)

    c_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
    f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    c_handler.setFormatter(c_format)
    f_handler.setFormatter(f_format)

    logger.addHandler(c_handler)
    logger.addHandler(f_handler)

    return logger


