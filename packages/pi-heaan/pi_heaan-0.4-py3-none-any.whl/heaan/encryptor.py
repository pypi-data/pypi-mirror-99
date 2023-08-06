
import numpy as np
from heaan import Context, Message, Ciphertext, EncryptionKey

class Encryptor:

    def __init__(self, context: Context):
        self._context = context
        pass

    def encrypt(self, message: Message, enc_key: EncryptionKey, ciphertext: Ciphertext) -> None:
        ciphertext._data = message._data.copy()
        ciphertext._number_of_slots = len(message)
        ciphertext._level = self._context.get_depth()

        self._context._update_op_history('encrypt   ')
        pass
