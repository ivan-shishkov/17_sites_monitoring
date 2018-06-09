import argparse
import os.path
import sys

from commonregex import CommonRegex
import requests
from requests.exceptions import ConnectionError


def execute_head_request(url):
    try:
        response = requests.head(url, allow_redirects=True)
        return response
    except ConnectionError:
        return None


def check_server_response_ok(url):
    response = execute_head_request(url)

    if response is None:
        return None

    return response.status_code == requests.codes.ok


def get_sites_urls(text):
    sites_links = CommonRegex(text).links

    sites_urls = []

    for link in sites_links:
        if link.startswith('http://') or link.startswith('https://'):
            sites_urls.append(link)
        else:
            sites_urls.append(''.join(('http://', link)))

    return sites_urls


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
