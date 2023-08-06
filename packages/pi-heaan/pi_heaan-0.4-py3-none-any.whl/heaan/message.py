
from typing import Union
import numpy as np

class Message:

    def __init__(self, data: list=[]):
        self._data = np.array(data)

    def __repr__(self):
        return repr(self._data)
    
    def __len__(self):
        return len(self._data)

    def __getitem__(self, index: int):
        return self._data[index]

    def __setitem__(self, index: int, value: Union[int, float]):
        self._data[index] = value
