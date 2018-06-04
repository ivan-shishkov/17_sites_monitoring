import argparse
import os.path
import sys


def load_text_data(filepath):
    if not os.path.exists(filepath):
        return None
    with open(filepath, 'r') as file:
        return file.read()


def parse_command_line_arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        'filename',
        help='a text file containing URLs of checked sites',
        type=str,
    )
    command_line_arguments = parser.parse_args()

    return command_line_arguments


def main():
    command_line_arguments = parse_command_line_arguments()

    filename = command_line_arguments.filename

    try:
        text = load_text_data(filename)
    except UnicodeDecodeError:
        sys.exit('text file has invalid format')

    if text is None:
        sys.exit('file not found')

    if not text:
        sys.exit('file is empty')


if __name__ == '__main__':
    main()
