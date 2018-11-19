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

# Launch inside a Docker container

For script launch inside a [Docker](https://www.docker.com/) container need to install Docker CE (e.g. [on Ubuntu](https://docs.docker.com/install/linux/docker-ce/ubuntu/)). Then clone this repository:

```bash

$ git clone https://github.com/ivan-shishkov/17_sites_monitoring.git

```

Go to the directory with downloaded repository:

```bash

$ cd 17_sites_monitoring/

```

And execute command to build image from Dockerfile:

```bash

$ sudo docker build -t sites-monitoring .

```

For script launch need to specify **absolute path** to the file with site's URLs and then execute command:

```bash

$ sudo docker run -it -v /absolute/path/to/sites_urls.txt:/data/sites.txt sites-monitoring

```

Example of script launch inside Docker container:

```bash

$ sudo docker run -it -v /home/user/sites_urls.txt:/data/sites.txt sites-monitoring
Checking sites...

Site URL: http://devman.org
Server response check result: OK (status code is 200)
Domain expiration date check result: Expires in more than 1 month

Site URL: http://python.ru
Server response check result: OK (status code is 200)
Domain expiration date check result: Expires in more than 1 month

Site URL: http://pythondigest.ru
Server response check result: OK (status code is 200)
Domain expiration date check result: Expires in more than 1 month

Site URL: http://dvmn.org
Server response check result: OK (status code is 200)
Domain expiration date check result: Expires in more than 1 month

```

# Project Goals

The code is written for educational purposes. Training course for web-developers - [DEVMAN.org](https://devman.org)
