import json

from collections import Counter
from constant import DECRYPTED_FILE, ENCRYPTED_FILE, KEY_FILE


def load_text(filename: str) -> str:
    """Загружает текст из файла"""
    with open(filename, "r", encoding="utf-8") as file:
        return file.read()


def save_text(filename: str, text: str) -> None:
    """Сохраняет текст в файл"""
    with open(filename, "w", encoding="utf-8") as file:
        file.write(text)


def save_json(filename: str, data: dict) -> None:
    """Сохраняет данные в JSON файл"""
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def calculate_char_frequency(text: str) -> list[tuple[str, int, float]]:
    """
    Подсчитывает частоту символов в тексте

    :param text: анализируемый текст
    :return: список кортежей
    """
    if not text:
        raise ValueError("Текст не может быть пустым")

    lower_text = text.lower()
    char_counter = Counter(lower_text)
    total_chars = len(lower_text)

    freq_with_percent = [
        (char, count, (count / total_chars) * 100)
        for char, count in char_counter.items()
    ]

    return sorted(freq_with_percent, key=lambda x: x[1], reverse=True)


def substitute_chars(text: str, substitution_key: dict[str, str]) -> str:
    """
    Заменяет символы

    :param text: исходный текст
    :param substitution_key: словарь
    :return: расшифрованный текст
    """
    decrypted_text = []

    for char in text:
        decrypted_text.append(substitution_key.get(char, char))

    return ''.join(decrypted_text)


def print_frequency_table(frequency_data: list[tuple[str, float]]) -> None:
    """Выводит таблицу частотности символов"""
    print("\nЧастота символов в зашифрованном тексте:")
    print("{:<10} {:<15}".format("Символ", "Процент (%)"))
    print("-" * 40)
    for char, count, percent in frequency_data[:20]:
        print("{:<10} {:<15.2f}".format(repr(char), percent))


def main():
    try:
        encrypted_text = load_text(ENCRYPTED_FILE)

        encrypted_freq = calculate_char_frequency(encrypted_text)
        print_frequency_table(encrypted_freq)

        with open(KEY_FILE, 'r', encoding='utf-8') as f:
            substitution_key = json.load(f)

        if not isinstance(substitution_key, dict):
            raise TypeError("Ключ замены должен быть словарем")

        decrypted_text = substitute_chars(encrypted_text, substitution_key)

        save_text(DECRYPTED_FILE, decrypted_text)


    except Exception as e:
        print(f"Произошла ошибка: {e}")
        return 1

    return 0


if __name__ == "__main__":
    main()