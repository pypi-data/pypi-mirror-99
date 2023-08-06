
import pickle
import numpy as np

class Ciphertext:

    # _FILE_SIZE = 48.3
    # _maximum_memory = 0
    # _current_memory = 0

    def __init__(self, number_of_primes: int=0, degree: int=0):
        # self._in_device = False
        self._level = 0
        self._number_of_slots = 0
        self._data = np.zeros(self._number_of_slots)
    
    def __repr__(self):
        status = dict()
        # status['in_device'] = self.in_device()
        status['level'] = self.get_level()
        status['num_slots'] = self.get_number_of_slots()
        
        return repr(status)

    def get_level(self):
        return self._level

    def get_min_level_for_bootstrap(self):
        return 4

    def get_number_of_slots(self):
        return self._number_of_slots

    def set_number_of_slots(self, number_of_slots):
        self._number_of_slots = number_of_slots

    def load(self, path):
        tmp = Ciphertext()
        with open(path, 'rb') as f:
            tmp = pickle.load(f)
        number_of_primes = tmp._number_of_primes
        degree = tmp._degree
        self.__init__(number_of_primes, degree)

        # self.to_device()
        # self._update_memory()
        pass
    
    def save(self, path):
        with open(path, 'wb') as f:
            pickle.dump(self, f)

        # if self.in_device:
        #     self.to_host()
        # self._update_memory()
        pass

    # def to_device(self):
    #     self._in_device = True
    #     Ciphertext._current_memory += Ciphertext._FILE_SIZE
    #     pass
    
    # def to_host(self):
    #     self._in_device = False
    #     Ciphertext._current_memory -= Ciphertext._FILE_SIZE
    #     pass

    # def in_device(self):
    #     return self._in_device

    # def _update_memory(self):
    #     if Ciphertext._current_memory > Ciphertext._maximum_memory:
    #         Ciphertext._maximum_memory = Ciphertext._current_memory