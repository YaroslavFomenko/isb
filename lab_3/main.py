import argparse
from generate_keys import KeyManager
from file_processing import FileManager
from asymmetrical import RSACrypto
from symmetrical import AESCrypto


class CryptoSystem:
    """Главная система гибридного шифрования"""

    def __init__(self, config_path):
        self.config = FileManager.load_config(config_path)

    def generate_keys(self):
        """Генерирует все необходимые ключи"""
        print("\n" + "=" * 50)
        print("ЗАПУСК ГЕНЕРАЦИИ КЛЮЧЕЙ")
        print("=" * 50)

        public_key, private_key = KeyManager.generate_key_pair()

        aes_key, iv = KeyManager.generate_aes_key()

        encrypted_aes_key = KeyManager.protect_aes_key(public_key, aes_key)

        FileManager.save_public_key(public_key, self.config['public_key_file'])
        FileManager.save_private_key(private_key, self.config['private_key_file'])
        FileManager.write_file(self.config['encrypted_key_file'], encrypted_aes_key)
        FileManager.write_file(self.config['iv_file'], iv)

        print("Все ключи успешно созданы и сохранены!")

    def encrypt_file(self):
        """Шифрует файл"""
        print("\n" + "=" * 50)
        print("ЗАПУСК ШИФРОВАНИЯ")
        print("=" * 50)

        private_key = FileManager.load_private_key(self.config['private_key_file'])
        encrypted_aes_key = FileManager.read_file(self.config['encrypted_key_file'])
        iv = FileManager.read_file(self.config['iv_file'])

        print("Восстанавливаем AES ключ...")
        aes_key = RSACrypto.rsa_decrypt(private_key, encrypted_aes_key)

        print("Читаем данные для шифрования...")
        plaintext = FileManager.read_file(self.config['source_file'])

        print("Шифруем данные AES...")
        ciphertext, _ = AESCrypto.encrypt_data(plaintext, aes_key, iv)

        FileManager.write_file(self.config['encrypted_file'], ciphertext)

        print("Файл успешно зашифрован!")

    def decrypt_file(self):
        """Расшифровывает файл"""
        print("\n" + "=" * 50)
        print("ЗАПУСК ДЕШИФРОВАНИЯ")
        print("=" * 50)

        private_key = FileManager.load_private_key(self.config['private_key_file'])
        encrypted_aes_key = FileManager.read_file(self.config['encrypted_key_file'])
        iv = FileManager.read_file(self.config['iv_file'])

        print("Восстанавливаем AES ключ...")
        aes_key = RSACrypto.rsa_decrypt(private_key, encrypted_aes_key)

        print("Читаем зашифрованные данные...")
        ciphertext = FileManager.read_file(self.config['encrypted_file'])

        print("Дешифруем данные AES...")
        plaintext = AESCrypto.decrypt_data(ciphertext, aes_key, iv)

        FileManager.write_file(self.config['decrypted_file'], plaintext)

        print("Файл успешно расшифрован!")


def main():

    parser = argparse.ArgumentParser(description="Система гибридного шифрования")

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-gen', action='store_true', help='Генерация ключей')
    group.add_argument('-enc', action='store_true', help='Шифрование файла')
    group.add_argument('-dec', action='store_true', help='Дешифрование файла')

    parser.add_argument('-c', '--config', required=True, help='Путь к конфигурации')

    args = parser.parse_args()

    try:
        system = CryptoSystem(args.config)

        if args.gen:
            system.generate_keys()
        elif args.enc:
            system.encrypt_file()
        elif args.dec:
            system.decrypt_file()

    except Exception as e:
        print(f"\nКритическая ошибка: {e}")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())