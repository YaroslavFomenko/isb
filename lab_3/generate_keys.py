from cryptography.hazmat.primitives.asymmetric import rsa
from asymmetrical import RSACrypto
from symmetrical import AESCrypto


class KeyManager:
    """Управление генерацией и защитой ключей"""

    @staticmethod
    def generate_key_pair(key_size=2048):
        """Создает пару RSA ключей"""
        print("Генерируем RSA ключи...")

        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=key_size
        )
        public_key = private_key.public_key()

        print(f"RSA-{key_size} ключи созданы")
        return public_key, private_key


    @staticmethod
    def generate_aes_key():
        """Создает AES ключ и IV"""
        print("Генерируем AES ключ...")

        aes_key = AESCrypto.create_aes_key(32)  # AES-256
        iv = AESCrypto.create_iv()

        print("AES ключ и IV созданы")
        return aes_key, iv


    @staticmethod
    def protect_aes_key(public_key, aes_key):
        """Защищает AES ключ RSA шифрованием"""

        encrypted_key = RSACrypto.rsa_encrypt(public_key, aes_key)
        print("AES ключ защищен")

        return encrypted_key

