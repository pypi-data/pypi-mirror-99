
import pandas as pd 
from heaan import Parameters

class Context:

    def __init__(self, params: Parameters=None, is_fixed_prime: bool=True):
        self._params = params

        self._is_bootstrappable = False
        self._op_history = dict()
        pass

    # estimated per mult at one core
    def __repr__(self):
        _op_time = {
            'encrypt   ': 0.370,
            'decrypt   ': 0.084,
            'add_const ': 0.013,
            'add       ': 0.023,
            'sub_const ': 0.013,
            'sub       ': 0.023,
            'mult_const': 0.121,
            'mult      ': 1,
            'rotate    ': 0.859,
            'bootstrap ': 114.898,
        }

        output  = "\n"
        output += "===== Operation Usage (in single thread) =====\n"

        total_time = 0
        df = pd.DataFrame(index=list(self._op_history.keys()))
        for op_type, op_num_usage in self._op_history.items():
            op_time_unit = _op_time[op_type]
            op_time_usage = op_time_unit * op_num_usage

            df.loc[op_type, "TIME_UNIT"] = op_time_unit
            df.loc[op_type, "NUM_USAGE"] = op_num_usage
            df.loc[op_type, "TIME_USAGE"]= op_time_usage

            total_time += op_time_usage
        
        output += repr(df)
        output += "\n----------------------------------------------\n"
        output += "\t*** Total estimated time unit : {}\n".format(total_time)

        # output += "\t*** Used memory : {} GB\n".format(Ciphertext._maximum_memory / 1000)

        return output

    def _update_op_history(self, op_type):
        if op_type in self._op_history:
            self._op_history[op_type] += 1
        else:
            self._op_history[op_type] = 1
        pass

    def get_degree(self):
        return self._params._degree

    def get_depth(self):
        return self._params._depth
    
    def get_quantize_bits(self):
        return self._params._quantize_bits

    def make_bootstrappable(self):
        self._is_bootstrappable = True
        pass

    def save_params(self, path):
        self._params.save(path)
        pass
    
    def load_params(self, path):
        self._params.load(path)
        pass
