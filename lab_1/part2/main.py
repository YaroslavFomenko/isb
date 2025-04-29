import json

from collections import Counter
from constant import RUS_FREQ, DECRYPTED_FILE, ENCRYPTED_FILE, KEY_FILE


def load_text(filename: str) -> str:
    """uploads text"""
    with open(filename, "r", encoding="utf-8") as file:
        return file.read()


def save_text(filename: str, text: str) -> None:
    """saves text"""
    with open(filename, "w", encoding="utf-8") as file:
        file.write(text)


def save_json(filename: str, data: dict) -> None:
    """saves data в JSON"""
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def analyze_and_decrypt(encrypted_text: str) -> tuple:
    """
    analyzes text and replaces characters

    :param encrypted_text: encrypted text
    :return: decrypted text and key
    """
    try:
        lower_text = encrypted_text.lower()
        total_chars = len(lower_text)
        if total_chars == 0:
            raise ValueError("Текст не может быть пустым")
        char_counter = Counter(lower_text)

        sorted_encrypted = sorted(
            char_counter.items(),
            key=lambda x: x[1],
            reverse=True
        )

        sorted_russian = sorted(
            RUS_FREQ.items(),
            key=lambda x: x[1],
            reverse=True
        )

        substitution_key = {}
        min_length = min(len(sorted_encrypted), len(sorted_russian))

        for i in range(min_length):
            encrypted_char = sorted_encrypted[i][0]
            russian_char = sorted_russian[i][0]
            substitution_key[encrypted_char] = russian_char

        decrypted_text = []
        for char in lower_text:
            if char in substitution_key:
                decrypted_text.append(substitution_key[char])
            else:
                decrypted_text.append(char)

        return ''.join(decrypted_text), substitution_key

    except Exception as e:
        print(f"Ошибка при анализе: {str(e)}")
        raise


def main():
    try:
        encrypted_text = load_text(ENCRYPTED_FILE)

        decrypted_text, substitution_key = analyze_and_decrypt(encrypted_text)

        save_text(DECRYPTED_FILE, decrypted_text)
        save_json(KEY_FILE, substitution_key)

        print("\nПример замены символов (первые 10 записей):")
        for i, (k, v) in enumerate(substitution_key.items()):
            if i >= 10:
                break
            print(f"{k} → {v}")

    except Exception as e:
        print(f"Произошла ошибка: {e}")
        return 1

    return 0


if __name__ == "__main__":
    main()
