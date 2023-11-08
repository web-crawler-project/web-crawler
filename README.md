# Web Crawler
___
Instructions:

1. Ensure you have Python 3 and `pip` installed. If not, download it from [here](https://www.python.org/downloads/).
2. In your terminal, run `pip install -r requirements.txt` to install the required packages
3. Navigate to the `input` directory and modify the `keywords.txt` and `urls.txt` files
    - `keywords.txt` should contain a list of keywords you wish to narrow your search to. 
       If left blank, the crawler will crawl all links on the page.
    - `urls.txt` should contain a list of seed URLs you wish to crawl
4. Navigate out of the directory and run `python3 main.py` to start the crawler
5. By default, the crawler has a limit of `10000` pages. You may modify this limit in `main.py`.
   Run `CTRL+C` to stop the crawler at any time.
6. Find the JSON output in the `output` directory
