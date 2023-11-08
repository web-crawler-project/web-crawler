import requests
import socket
import json
from time import sleep
from bs4 import BeautifulSoup
from urllib.parse import urlparse


def scrape_website(url):
    try:

        # Set the headers pretending to be a browser, to avoid 403 Forbidden response
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36',
        }

        response = requests.get(url, headers=headers, timeout=5)

        # Check if the request was accepted but not yet processed, wait and probe one more time
        if response.status_code == 202:
            sleep(3)
            response = requests.get(url, headers=headers, timeout=5)

        # Check if the request was successful
        if response.status_code == 200:
            time = response.elapsed.total_seconds()
            parsed_url = urlparse(url)
            ip = socket.gethostbyname(parsed_url.netloc)
            geo = get_geolocation(ip)
            # Parse the HTML content of the page using BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')

            return soup, time, ip, geo


    except requests.exceptions.RequestException as e:
        pass


def get_geolocation(ip_address):
    url = 'https://api.findip.net/' + ip_address + '/?token=20a4a32e0aee4d5595527acb1d23fcfe'
    response = requests.get(url)
    result = response.content.decode()
    data = json.loads(result)
    return data['location']
