
import pickle
from heaan import Context

class SecretKey:

    def __init__(self, context: Context=None):
        self._context = context
        pass

    def load(self, path):
        tmp = SecretKey()
        with open(path, 'rb') as f:
            tmp = pickle.load(f)
        context = tmp._context
        self.__init__(context)
        pass
    
    def save(self, path):
        with open(path, 'wb') as f:
            pickle.dump(self, f)
        pass
