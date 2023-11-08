import os
from urllib.parse import urlparse
import re


# Function to extract data (headers, paragraphs) and links from HTML
# @param soup: BeautifulSoup Object which stores HTML content
# @return: JSON data and links
def extract_html(soup, keywords):
    extracted_data = {}

    # Extract headers
    headers = []
    for header in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
        if header.get_text():
            headers.append(header.get_text().strip())

    if headers and keywords:
        if not contain_keyword(headers, keywords):
            return None, None

        extracted_data['headers'] = headers

    # Extract paragraph data
    paragraphs = []
    for paragraph in soup.find_all('p'):
        if paragraph.get_text():
            paragraphs.append(paragraph.get_text().strip())

    if paragraphs:
        extracted_data['paragraphs'] = paragraphs

    # Extract links
    links = []
    for link in soup.find_all('a', href=True):
        # Filter only http or https urls
        if link['href'].startswith('http') and check_html_link(link['href']):
            links.append(link['href'])

    return extracted_data, links


def contain_keyword(headers, keywords):
    headers_split = []
    for header in headers:
        raw_split_header = header.lower().split()
        for word in raw_split_header:
            headers_split.append(re.sub(r'\W+', '', word))

    for header in headers_split:
        if header in keywords:
            return True
    return False


def check_html_link(url):
    parsed_url = urlparse(url)
    path = parsed_url.path
    filename, file_extension = os.path.splitext(path)
    if file_extension:
        return False
    return True
