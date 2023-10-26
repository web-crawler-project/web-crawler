Instructions for `html_extractor.py`

1) In your terminal, run `sudo apt-get install python3-bs4` first to install BeautifulSoup HTML parser
2) Parse in your HTML content into `extract_html` function
3) Output will be (JSON_data, links)
     - JSON_data will be in JSON format, comprising of:
         - A list of all `headers` found (h1, h2, h3, h4, h5, h6)**
         - A list of all `paragraphs` found
     - Links is a list of `http://` and `https://` hyperlinks found in the document

** Decided to have a separate header list because headers might help to summarize contents in the body (? Not sure how we wanna process the data)
