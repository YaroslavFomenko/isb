from constants import *

import math
import numpy as np
from scipy.special import gammainc, erfc


def read_file(filename):
    """
    читает содержимое файла
    """
    try:
        with open(filename, 'r') as f:
            return f.read().strip()
    except FileNotFoundError:
        print(f"\nError: File {filename} not found!")
        return None
    except Exception as e:
        print(f"\nError reading {filename}: {str(e)}")
        return None


def write_to_file(filename, content_1, content_2, content_3):
    """
    Записывает результаты тестов в файл
    """
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(f"1. Frequency Test p-value: {content_1}\n")
        file.write(f"2. Runs Test p-value: {content_2}\n")
        file.write(f"3. Longest Run of Ones Test p-value: {content_3}\n")


def frequency_test(bits):
    """
    Частотный побитовый тест.
    :param bits: битовая последовательность
    :return: Р-значение
    """
    n = len(bits)
    sum_bits = sum(int(b) for b in bits)
    s = (2 * sum_bits - n) / math.sqrt(n)
    p_value = erfc(abs(s) / math.sqrt(2))
    return p_value



def runs_test(bits):
    """
    Тест на одинаковые подряд идущие биты.
    :param bits: битовая последовательность
    :return: Р-значение
    """
    n = len(bits)
    pi = sum(int(b) for b in bits) / n

    if abs(pi - 0.5) >= 2 / math.sqrt(n):
        return 0.0

    v_obs = 0
    for i in range(0, n-1):
        if bits[i] != bits[i + 1]:
            v_obs += 1

    numerator = abs(v_obs - 2 * n * pi * (1 - pi))
    denominator = 2 * math.sqrt(2 * n) * pi * (1 - pi)
    p_value = erfc(numerator / denominator)
    return p_value

def longest_run_ones_test(bits, block_size=8):
    """
    Тест на самую длинную последовательность единиц в блоке.
    :param bits: битовая последовательность
    :param block_size: размер блоков
    :return: Р-значение
    """
    n = len(bits)
    if n < block_size:
        return 0.0

    num_blocks = n // block_size
    blocks = np.array([int(b) for b in bits[:num_blocks * block_size]]).reshape((num_blocks, block_size))

    max_runs = []
    for block in blocks:
        current_run = 0
        max_run = 0
        for bit in block:
            if bit == 1:
                current_run += 1
                if current_run > max_run:
                    max_run = current_run
            else:
                current_run = 0
        max_runs.append(max_run)

    if block_size == 8:
        K = 3
        pi = [0.2148, 0.3672, 0.2305, 0.1875]
        categories = [1, 2, 3, 4]  # 1, 2, 3, 4+
    else:
        return 0.0

    v = [0] * len(categories)
    for run in max_runs:
        if run <= 1:
            v[0] += 1
        elif run == 2:
            v[1] += 1
        elif run == 3:
            v[2] += 1
        else:  # run >= 4
            v[3] += 1

    chi_square = sum((v[i] - num_blocks * pi[i]) ** 2 / (num_blocks * pi[i]) for i in range(len(categories)))

    p_value = gammainc(K / 2, chi_square / 2)

    return p_value


def test_sequence(input_file, output_file):
    """
    проверка тестов и сохранение результатов в файлы
    """
    bits_str = read_file(input_file)
    if bits_str is None:
        return

    bits = list(bits_str)

    p1 = frequency_test(bits)
    p2 = runs_test(bits)
    p3 = longest_run_ones_test(bits)

    write_to_file(output_file, p1, p2, p3)

    print(f"\nTesting sequence from {input_file}")
    print(f"1. Frequency Test p-value: {p1:.6f}")
    print(f"2. Runs Test p-value: {p2:.6f}")
    print(f"3. Longest Run of Ones Test p-value: {p3:.6f}")


if __name__ == "__main__":
    test_sequence(PATH_TO_CPP_SEQ, PATH_TO_NIST_RES_CPP)
    test_sequence(PATH_TO_JAVA_SEQ, PATH_TO_NIST_RES_JAVA)
    print("\nTesting completed. Results saved to output files.")