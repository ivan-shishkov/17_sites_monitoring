# Sites Monitoring Utility

This script is intended for monitoring of sites state by checking that:

* response status code of the server is equal to 200 (HTTP OK)
* domain name expires in more than 1 month

# Quickstart

For script launch need to install Python 3.5 and then install all dependencies:

```bash

$ pip install -r requirements.txt

```

Usage:

```bash

$ python3 check_sites_health.py -h
usage: check_sites_health.py [-h] filename

positional arguments:
  filename    a text file containing URLs of checked sites

optional arguments:
  -h, --help  show this help message and exit

```

Example of script launch on Linux:

```bash

$ python3 check_sites_health.py sites_urls.txt
Checking sites...

Site URL: http://devman.org
Server response check result: OK (status code is 200)
Domain expiration date check result: Expires in more than 1 month

Site URL: http://pythonz.net
Server response check result: OK (status code is 200)
Domain expiration date check result: Expires in more than 1 month

Site URL: http://qazxsw.ru
Server response check result: Could not get response
Domain expiration date check result: Could not get info about expiration date

```

# Project Goals

The code is written for educational purposes. Training course for web-developers - [DEVMAN.org](https://devman.org)
