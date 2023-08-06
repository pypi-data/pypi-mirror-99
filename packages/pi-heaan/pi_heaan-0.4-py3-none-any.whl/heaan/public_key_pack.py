
import os
from heaan import Context, \
                SecretKey, \
                EncryptionKey, \
                RelinearlizationKey, \
                ConjugationKey, \
                RotationKey

class PublicKeyPack:

    def __init__(self, context: Context, secret_key: SecretKey, public_keypack_path: str):
        self._context = context
        self._rot_key_idx = [
            1,     2,     3,     4,     5,     6,     7,     8,     16,    24,    32,
            40,    48,    56,    64,    96,    128,   160,   192,   224,   256,   512,
            768,   1024,  1280,  1536,  1792,  2048,  3072,  4096,  5120,  6144,  7168,
            8192,  16384, 24576, 32768, 40960, 49152, 57344, 61440, 63488, 64512, 64544,
            65024, 65280, 65408, 65472, 65504, 65505, 65520, 65528, 65532, 65534, 65535
        ]

        self.set_key_dir_path(public_keypack_path)
        self.generate_encryption_key(secret_key)
        self.generate_multiplication_key(secret_key)
        self.generate_conjugation_key(secret_key)
        self.generate_rotation_key(secret_key)
        pass

    def set_key_dir_path(self, public_keypack_path):
        os.makedirs(name=public_keypack_path+"/PK/", mode=0o775, exist_ok=True)
        self._public_keypack_path = public_keypack_path
        pass

    def get_key_dir_path(self):
        return self._public_keypack_path

    def get_enc_key(self):
        enc_key = EncryptionKey()
        path = self.get_key_dir_path() + "/PK/EncKey.bin"
        enc_key.load(path)
        return enc_key

    def get_mult_key(self):
        mult_key = RelinearlizationKey()
        path = self.get_key_dir_path() + "/PK/MultKey.bin"
        mult_key.load(path)
        return mult_key
    
    def get_conj_key(self):
        conj_key = ConjugationKey()
        path = self.get_key_dir_path() + "/PK/ConjKey.bin"
        conj_key.load(path)
        return conj_key

    def get_left_rot_key(self, idx):
        half_degree = self._context.get_degree() // 2
        while idx < 0:
            idx += half_degree
        idx %= half_degree

        if idx not in self._rot_key_idx:
            raise IndexError

        rot_key = RotationKey()
        rot_key.load(self.get_key_dir_path() + "/PK/RotKey" + str(idx) + ".bin")
        return rot_key

    def get_right_rot_key(self, idx):
        return self.get_left_rot_key(-idx)

    def load(self, public_keypack_path):
        self.set_key_dir_path(public_keypack_path)
        pass

    def generate_encryption_key(self, secret_key):
        enc_key = EncryptionKey()
        enc_key.save(self._context, self._public_keypack_path + "/PK/EncKey.bin")
        pass
    
    def generate_multiplication_key(self, secret_key):
        mult_key = RelinearlizationKey()
        mult_key.save(self._context, self._public_keypack_path + "/PK/MultKey.bin")
        pass

    def generate_conjugation_key(self, secret_key):
        conj_key = ConjugationKey()
        conj_key.save(self._context, self._public_keypack_path + "/PK/ConjKey.bin")
        pass

    def generate_rotation_key(self, secret_key):
        for idx in self._rot_key_idx:
            rot_key = RotationKey()
            rot_key.save(self._context, self._public_keypack_path + "/PK/RotKey" + str(idx) + ".bin")
        pass
