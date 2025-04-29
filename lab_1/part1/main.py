import argparse

from encryption import cipher, read_file, write_file


def parsing():
    parser = argparse.ArgumentParser(description="Encrypt text.")
    parser.add_argument('input_file', type=str, help="Path to the input text file.")
    parser.add_argument('output_file', type=str, help="Path to the output text file.")
    parser.add_argument('key_file', type=str, help="Path to the encryption key.")
    return parser


def main():
    parser = parsing()
    args = parser.parse_args()
    try:
        key = read_file(args.key_file)
        input_text = read_file(args.input_file)

        if not key:
            raise ValueError("The encryption key cannot be empty.")
        if not input_text:
            raise ValueError("The input text cannot be empty.")

        result_text = cipher(input_text, key)
        write_file(args.output_file, result_text)
        print(f"Encription is complited")
    except ValueError as e:
        print(f"Error: {e}")
    except FileNotFoundError as e:
        print(f"File error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()