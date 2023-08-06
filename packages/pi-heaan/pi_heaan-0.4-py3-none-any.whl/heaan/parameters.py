
import math
import pickle

class Parameters:

    def __init__(self, log_degree: int=17, depth: int=29, quantize_bits: int=51, dnum: int=3):
        self._depth = depth
        self._log_degree = log_degree
        self._degree = 2 ** log_degree
        self._dnum = dnum
        self._quantize_bits = quantize_bits
        
        # self._is_gpu = False
        pass

    def get_degree(self):
        return self._degree

    def get_quantize_bits(self):
        return self._quantize_bits

    def load(self, path):
        tmp = Parameters()
        with open(path, 'rb') as f:
            tmp = pickle.load(f)
        log_degree = tmp._log_degree
        depth = tmp._depth
        quantize_bits = tmp._quantize_bits
        dnum = tmp._dnum
        self.__init__(log_degree, depth, quantize_bits, dnum)
        pass
    
    def save(self, path):
        with open(path, 'wb') as f:
            pickle.dump(self, f)
        pass

    # def _set_gpu(self):
    #     self._is_gpu = True
    #     pass
