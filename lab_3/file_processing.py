import json

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.serialization import load_pem_public_key, load_pem_private_key


class FileManager:
    """Управление файловыми операциями"""

    @staticmethod
    def read_file(filename):
        """Читает файл"""
        try:
            with open(filename, 'rb') as f:
                return f.read()
        except FileNotFoundError:
            print(f"Файл не найден: {filename}")
            raise
        except Exception as e:
            print(f"Ошибка чтения файла: {e}")
            raise


    @staticmethod
    def write_file(filename, data):
        """Записывает данные в файл"""
        try:
            with open(filename, 'wb') as f:
                f.write(data)
            print(f"Данные сохранены в: {filename}")
        except Exception as e:
            print(f"Ошибка записи файла: {e}")
            raise


    @staticmethod
    def load_config(config_path):
        """Загружает конфигурацию"""
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Ошибка загрузки конфигурации: {e}")
            raise


    @staticmethod
    def save_public_key(key, filename):
        """Сохраняет публичный ключ"""
        try:
            pem_data = key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            )
            FileManager.write_file(filename, pem_data)
        except Exception as e:
            print(f"Ошибка сохранения публичного ключа: {e}")
            raise


    @staticmethod
    def save_private_key(key, filename):
        """Сохраняет приватный ключ"""
        try:
            pem_data = key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption()
            )
            FileManager.write_file(filename, pem_data)
        except Exception as e:
            print(f"Ошибка сохранения приватного ключа: {e}")
            raise


    @staticmethod
    def load_public_key(filename):
        """Загружает публичный ключ"""
        try:
            key_data = FileManager.read_file(filename)
            return load_pem_public_key(key_data)
        except Exception as e:
            print(f"Ошибка загрузки публичного ключа: {e}")
            raise


    @staticmethod
    def load_private_key(filename):
        """Загружает приватный ключ"""
        try:
            key_data = FileManager.read_file(filename)
            return load_pem_private_key(key_data, password=None)
        except Exception as e:
            print(f"Ошибка загрузки приватного ключа: {e}")
            raise