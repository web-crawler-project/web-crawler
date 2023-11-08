import os
from urllib.parse import urlparse
import re


# Function to extract data (headers, paragraphs) and links from HTML
# @param soup: BeautifulSoup Object which stores HTML content
# @return: JSON data and links
def extract_html(soup, keywords):
    extracted_data = {}

    # Extract HTML headers from h1 to h6
    headers = []
    for header in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
        if header.get_text():
            headers.append(header.get_text().strip())

    if headers and keywords:
        # Check if headers do not contain any keyword specified
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

    # Extract hyperlinks from page
    links = []
    for link in soup.find_all('a', href=True):
        # Filter only http or https urls with no extensions
        if link['href'].startswith('http') and check_html_link(link['href']):
            links.append(link['href'])

    # Return the data extracted (headers and paragraphs), with the links found
    return extracted_data, links

# Function to check if any of the headers contain a keyword specified
def contain_keyword(headers, keywords):
    headers_split = []
    for header in headers:
        raw_split_header = header.lower().split()
        for word in raw_split_header:
            # Remove all non-alphanumerical characters
            headers_split.append(re.sub(r'\W+', '', word))

    for header in headers_split:
        if header in keywords:
            return True
    return False

# Function to check if parsed url does not contain any extension
def check_html_link(url):
    parsed_url = urlparse(url)
    path = parsed_url.path
    filename, file_extension = os.path.splitext(path)
    if file_extension:
        return False
    return True
