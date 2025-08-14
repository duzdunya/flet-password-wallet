from typing import NoReturn
import os
import json

def load_data(path: str, return_format: str) -> T:
    if os.path.isfile(path):
        if os.path.exists(path):
            pass
        else:
            raise FileNotFoundError()


def save_data(content:T, path: str) -> NoReturn:
    if os.path.isfile(path):
        if os.path.exists(path):
            pass
        else:
            raise FileNotFoundError()

