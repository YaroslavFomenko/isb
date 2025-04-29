from constant import ALPHABET, ALPHABET_SIZE


def get_encryption_char(text_char: str, key_char: str) -> str:
    """
    encrypts a single symbol
    :param text_char: character text
    :param key_char: character key
    :return: encryption symbol
    """

    if text_char.lower() not in ALPHABET:
        return text_char

    try:
        text_pos = ALPHABET.index(text_char.lower())
        key_pos = ALPHABET.index(key_char.lower())
    except ValueError as e:
        raise ValueError("Error searching for character in alphabet") from e

    encrypted_pos = (text_pos + key_pos) % ALPHABET_SIZE

    encrypted_char = ALPHABET[encrypted_pos]
    return encrypted_char.upper() if text_char.isupper() else encrypted_char


def cipher(text: str, key: str) -> str:
    """
    Encrypts the text using the Trithemius cipher
    :param text:  original text
    :param key: key cipher
    :return: encrypted text
    """
    if not text:
        raise ValueError("The text to encrypt cannot be empty.")
    if not key:
        raise ValueError("The encryption key cannot be empty.")

    encrypted_text = []
    key_length = len(key)
    key_pos = 0

    for char in text:
        current_key_char = key[key_pos % key_length]

        encrypted_char = get_encryption_char(char, current_key_char)
        encrypted_text.append(encrypted_char)

        if char.lower() in ALPHABET:
            key_pos += 1

    return ''.join(encrypted_text)


def read_file(file: str) -> str:
    """
    read file
    :param file: original file
    """
    try:
        with open(file, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"File not found: {file}")
    except Exception as e:
        print(f"Error reading file '{file}': {e}")


def write_file(file_path: str, content: str) -> None:
    """
    Writes a file.
    :param file_path: original file.
    :param content: file to be written.
    """
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)
    except Exception as e:
        print(f"Error writing to file '{file_path}': {e}")
