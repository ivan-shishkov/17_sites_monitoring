import argparse
import os.path
import sys
import socket
from datetime import datetime, timedelta

from commonregex import CommonRegex
import requests
from requests.exceptions import ConnectionError
from whois import whois


def check_server_response_ok(url):
    try:
        response = requests.get(url)
        return response.ok
    except ConnectionError:
        return None


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
    links = CommonRegex(text).links

    sites_urls = []

    for link in links:
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
        server_response_check_result = check_server_response_ok(site_url)
        domain_expiration_date_check_result = check_domain_expiration_date(
            url=site_url,
        )
        sites_check_results[site_url] = (
            server_response_check_result,
            domain_expiration_date_check_result,
        )
    return sites_check_results


def get_description_check_response(check_result):
    response_check_result_descriptions = {
        None: 'Could not get response',
        True: 'OK (status code is 200)',
        False: 'BAD (status code is not 200)',
    }
    return response_check_result_descriptions[check_result]


def get_description_check_expiration_date(check_result):
    expiration_date_check_result_descriptions = {
        None: 'Could not get info about expiration date',
        True: 'Expires in more than 1 month',
        False: 'Expires in less than 1 month',
    }
    return expiration_date_check_result_descriptions[check_result]


def print_site_check_results(site_check_results):
    response_check_result, expiration_date_check_result = site_check_results
    print('Server response check result: {}'.format(
        get_description_check_response(response_check_result),
    ))
    print('Domain expiration date check result: {}'.format(
        get_description_check_expiration_date(expiration_date_check_result),
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
