from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from typing import Any


class RSACrypto:
    """Обработчик RSA шифрования для защиты ключей"""

    @staticmethod
    def rsa_encrypt(public_key: Any, data: bytes) -> bytes:
        """
        Шифрует данные RSA публичным ключом.
        Использует OAEP padding с SHA256 для надежности.
        :param public_key: публичный ключ
        :param data: данные для шифрования
        :return: зашифрованные данные
        """
        try:
            print("Начинаем RSA шифрование...")

            encrypted = public_key.encrypt(
                data,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )

            print("RSA шифрование завершено")
            return encrypted

        except ValueError as e:
            print(f"Слишком много данных для RSA: {e}")
            raise
        except Exception as e:
            print(f"Ошибка RSA шифрования: {e}")
            raise


    @staticmethod
    def rsa_decrypt(private_key: Any, encrypted_data: bytes) -> bytes:
        """
         Расшифровывает данные RSA приватным ключом
        :param private_key: приватный ключ
        :param encrypted_data: зашифрованные данные
        :return: расшифрованные данные
        """

        try:
            print("Начинаем RSA дешифрование...")

            decrypted = private_key.decrypt(
                encrypted_data,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )

            print("RSA дешифрование завершено")
            return decrypted

        except Exception as e:
            print(f"Ошибка RSA дешифрования: {e}")
            raise