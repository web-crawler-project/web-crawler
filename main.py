import json
import queue

# Read urls from input file, returns an array of urls
# Only reads unique urls (assuming there can be duplicate urls in the file)
def read_urls():
  urls = queue.Queue()
  seen_urls = set()
  
  try:
    # TODO: Use file access lock mechanism
    with open(input_file, 'r') as file:
      for line in file:
        url = line.strip()
        if url and url not in seen_urls:
          urls.put(url)
          seen_urls.add(url)
  except IOError as e:
    print(f'Error reading {input_file}: {e}')
    
  return urls

# Returns unique urls in data that hasnt been crawled
# Compare with urls in urls.txt file
# Instead of keeping track of the url in program for multithreading purposes
# Instead of data.json file, assuming data.json and urls.txt are in sync
def remove_duplicate_urls(data):
  current_urls = read_urls()
  unique_data = [d for d in data if not any(url in current_urls.queue for url in d) and d]
  return unique_data

# Writes unique urls to urls.txt
def write_urls(data):
  urls = [key for d in data for key in d.keys()]
  print(f'Writing the following urls to {input_file}: {urls}')
  
  try:
    # TODO: Use file access lock mechanism
    with open(input_file, 'a') as file:
      for url in urls:
        file.write(f'{url}\n')
  except IOError as e:
    print(f'Error writing {output_file}: {e}')

# Only write unique url and data to the output file
# Assuming data originated from the url that just got scraped
def write_data(new_data, origin_url):
  try:
    # TODO: Use file access lock mechanism
    with open(output_file, 'r+') as file:
      try:
        # Read existing JSON data
        json_data = json.load(file)
      except json.JSONDecodeError:
        # If file is empty, initialize with empty JSON data
        json_data = {}
      
      # Append new URLs to JSON data
      print(f'Writing the following urls to {output_file}:')
      for one_new_data in new_data:
        print(one_new_data)
        for url, xml in one_new_data.items():
          json_data[url] = {'xml': xml, 'origin': origin_url}
      
      # Write updated JSON data to file
      file.seek(0)
      json.dump(json_data, file, indent=2)
      file.truncate()
  except IOError as e:
    print(f'Error writing {output_file}: {e}')

if __name__ == '__main__':
  # Global variables
  input_file = './urls.txt'
  output_file = './data.json'
  
  # urls - queue variable
  urls = read_urls()
  
  # Process each url
  # TODO: Incorporate multiprocessing here
  while not urls.empty():
    url = urls.get()
    print(f'Processing {url}...')
    
    # TODO: Crawl with the url and get back an array of {'new url': 'xml data'}
    # New url to strip trailing '/'
    # Assuming data only has unique links
    data = [{'www.google.com': 'xml'}, {'www.apple.com': 'xml'},
            {'www.test.com': 'xml'}, {'www.orange.com': 'xml'}]
    
    # unique_data - array of {'new url': 'xml data'}
    unique_data = remove_duplicate_urls(data)
    write_urls(unique_data)
    write_data(unique_data, url)
    
    # TODO: Add criteria to end the program (break from loop) if necessary
