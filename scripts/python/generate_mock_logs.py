import logging
import random

urls = [
    "/~vartiukhov",
    "/~vartiukhov/src/css/margins.css",
    "/~vartiukhov/src/css/normilize.css",
    "/~vartiukhov/src/pages/dashboard.html",
    "/~vartiukhov/src/css/modal.css",
    "/~vartiukhov/src/js/dashboard.js",
    "/~vartiukhov/src/js/implementation.js",
    "/~vartiukhov/src/css/styles.css",
    "/~vartiukhov/src/assets/icons/logo-icon.svg",
    "/~vartiukhov/src/assets/images/cameras.jpg",
    "/~vartiukhov/src/assets/icons/globe-icon.svg"
]

ips = [
    '10.82.167.23',
    '10.82.167.205',
    '10.82.167.12',
    '10.82.162.19',
    '10.82.17.12',
    '10.1.17.1',
    '10.82.100.222',
    '12.32.32.111',
    '12.8.17.12',
    '12.8.101.100',
    '12.8.111.220'
]

status_codes = [
    200, 203, 301, 303, 400, 404, 500, 503, 302, 201
]

methods = [
    'GET', 'POST', 'PUT', 'PATCH', 'DELETE'
]

dates = [
    '21/Nov/2023:21:31:45 +0100',
    '21/Nov/2023:15:44:43 +0100',
    '21/Nov/2023:00:00:45 +0100',
    '21/Nov/2023:11:11:15 +0100',
    '21/Nov/2023:15:44:15 +0100',
    '20/Nov/2023:22:00:12 +0100',
    '20/Nov/2023:08:32:06 +0100',
    '20/Nov/2023:12:12:00 +0100',
    '20/Nov/2023:19:33:33 +0100',
    '20/Nov/2023:12:00:55 +0100',
]

browsers = [
    '"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"',
    'Mozilla/5.0 (Windows; U; Windows NT 6.0; en-us; rv:1.9.2.3) Gecko/20100401 WINFC 2.0.0.1 Firefox/3.6.3 (.NET CLR 3.5.30729)',
    'Opera/9.80 (Windows NT 6.0) Presto/2.12.388 Version/12.14',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134',
    'Mozilla/5.0 (Windows; U; Windows NT 6.0; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
]

# number of logs to generate
COUNT = 120
# filepath where to store the logs
FILEPATH = "access.log"

# Set up logging
logging.basicConfig(filename=FILEPATH, level=logging.INFO, format='%(message)s')

# Generate 40 logs with random URLs
for _ in range(COUNT):
    url = random.choice(urls)
    ip = random.choice(ips)
    status_code = random.choice(status_codes)
    method = random.choice(methods)
    date = random.choice(dates)
    browser = random.choice(browsers)

    logging.info(f"{ip} - - [{date}] \"{method} {url} HTTP/1.1\" {status_code} 0 \"-\" \"{browser}\"")
