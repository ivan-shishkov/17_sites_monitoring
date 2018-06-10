import argparse
import os.path
import sys
import socket
from datetime import datetime, timedelta

from commonregex import CommonRegex
import requests
from requests.exceptions import ConnectionError
from whois import whois


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


def get_whois_info(url):
    try:
        whois_info = whois(url)
        return whois_info
    except socket.gaierror:
        return None


def get_domain_expiration_date(domain_whois_info):
    expiration_date = domain_whois_info.expiration_date

    if isinstance(expiration_date, list):
        return expiration_date[0]
    else:
        return expiration_date


def check_domain_expiration_date(url, min_remaining_time=timedelta(days=30)):
    domain_whois_info = get_whois_info(url)

    if domain_whois_info is None:
        return None

    domain_expiration_date = get_domain_expiration_date(domain_whois_info)

    if domain_expiration_date is None:
        return None

    return domain_expiration_date > datetime.now() + min_remaining_time


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


def get_sites_check_results(sites_urls):
    sites_check_results = {}

    for site_url in sites_urls:
        result_check_response_ok = check_server_response_ok(site_url)
        result_check_domain_expiration_date = check_domain_expiration_date(
            url=site_url,
        )
        sites_check_results[site_url] = (
            result_check_response_ok,
            result_check_domain_expiration_date,
        )
    return sites_check_results


def get_description_check_response(check_response_result):
    descriptions_check_response = {
        None: 'Could not get response',
        True: 'OK (status code is 200)',
        False: 'BAD (status code is not 200)',
    }
    return descriptions_check_response[check_response_result]


def get_description_check_expiration_date(check_expiration_date_result):
    if check_expiration_date_result is None:
        return 'Could not get info about expiration date'

    if check_expiration_date_result:
        return 'Great than 1 month'
    else:
        return 'Less than 1 month'


def print_site_check_results(site_check_results):
    check_response_result, check_expiration_date_result = site_check_results
    print('Server response check result: {}'.format(
        get_description_check_response(check_response_result),
    ))
    print('Domain expiration date check result: {}'.format(
        get_description_check_expiration_date(check_expiration_date_result),
    ))


def print_sites_check_results(sites_check_results):
    for site_url in sorted(sites_check_results.keys()):
        print('\nSite URL: {}'.format(site_url))
        print_site_check_results(sites_check_results[site_url])


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

    print('Checking sites...')

    sites_check_results = get_sites_check_results(
        sites_urls=get_sites_urls(text),
    )

    print_sites_check_results(
        sites_check_results=sites_check_results,
    )


if __name__ == '__main__':
    main()
