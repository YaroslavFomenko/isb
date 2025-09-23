import os

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding


class AESCrypto:
    """AES шифрование с CBC режимом для данных"""

    @staticmethod
    def create_iv():
        """Создает случайный вектор инициализации"""
        return os.urandom(16)


    @staticmethod
    def create_aes_key(key_size=32):
        """Генерирует AES ключ нужного размера"""
        if key_size not in [16, 24, 32]:
            raise ValueError("Допустимые размеры ключа: 16, 24, 32 байта")
        return os.urandom(key_size)


    @staticmethod
    def encrypt_data(data: bytes, key: bytes, iv: bytes = None) -> tuple:
        """
        Шифрует данные AES-256 в режиме CBC
        Возвращает (шифротекст, iv)
        """
        try:
            if iv is None:
                iv = AESCrypto.create_iv()

            if len(key) not in [16, 24, 32]:
                raise ValueError("Неверный размер AES ключа")

            cipher = Cipher(
                algorithms.AES(key),
                modes.CBC(iv),
                backend=default_backend()
            )

            padder = padding.PKCS7(128).padder()
            padded_data = padder.update(data) + padder.finalize()

            encryptor = cipher.encryptor()
            ciphertext = encryptor.update(padded_data) + encryptor.finalize()

            print("AES шифрование успешно")
            return ciphertext, iv

        except Exception as e:
            print(f"Ошибка AES шифрования: {e}")
            raise


    @staticmethod
    def decrypt_data(ciphertext: bytes, key: bytes, iv: bytes) -> bytes:
        """
        Расшифровывает данные AES
        """
        try:
            cipher = Cipher(
                algorithms.AES(key),
                modes.CBC(iv),
                backend=default_backend()
            )

            decryptor = cipher.decryptor()
            padded_data = decryptor.update(ciphertext) + decryptor.finalize()

            unpadder = padding.PKCS7(128).unpadder()
            plaintext = unpadder.update(padded_data) + unpadder.finalize()

            print("AES дешифрование успешно")
            return plaintext

        except Exception as e:
            print(f"Ошибка AES дешифрования: {e}")
            raise