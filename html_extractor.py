import json
from bs4 import BeautifulSoup

# Function to extract data (headers, paragraphs) and links from HTML
# @param html_content: HTML content of the page
# @return: JSON data and links
def extract_html(html_content):
    # Create a BeautifulSoup object from html content
    soup = BeautifulSoup(html_content, 'html.parser')

    extracted_data = {}

    # Extract headers
    headers = []
    for header in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
        if header.get_text():
            headers.append(header.get_text().strip())

    if headers:
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
        if link['href'].startswith('http'):
            links.append(link['href'])

    # Convert data to JSON
    json_data = json.dumps(extracted_data)

    return json_data, links
