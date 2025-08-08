from typing import Union

class Local:
    def __init__(self, d:Union[dict, None]=None):
        if d is not None:
            for key, value in d.items():
                setattr(self, key, value)
