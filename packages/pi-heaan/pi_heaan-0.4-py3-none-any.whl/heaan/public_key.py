
import pickle
from heaan import Context

class EncryptionKey:

    def __init__(self):
        self._key_id = 0

    def load(self, path: str):
        tmp = EncryptionKey()
        with open(path, 'rb') as f:
            tmp = pickle.load(f)
        self.__init__()
        pass
    
    def save(self, context: Context, path: str):
        with open(path, 'wb') as f:
            pickle.dump(self, f)
        pass

class EvaluationKey:

    def __init__(self):
        self._key_id = -999

    def get_evaluation_key_id(self):
        return self._key_id

    def load(self, path: str):
        tmp = EvaluationKey()
        with open(path, 'rb') as f:
            tmp = pickle.load(f)
        self.__init__()
        pass
    
    def save(self, context: Context, path: str):
        with open(path, 'wb') as f:
            pickle.dump(self, f)
        pass

class RelinearlizationKey(EvaluationKey):

    def get_evaluation_key_id(self):
        return 0

class ConjugationKey(EvaluationKey):

    def get_evaluation_key_id(self):
        return -1

class RotationKey(EvaluationKey):

    pass
