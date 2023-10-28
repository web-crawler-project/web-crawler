import json
import queue

# Returns a set of unique urls that are already in data.json
def read_processed_urls():
  json_data = {}
  try:
    with open(output_file, 'r') as file:
      try:
        # Read existing JSON data
        json_data = json.load(file)
      except json.JSONDecodeError:
        pass
  except IOError as e:
    print(f'Error reading {output_file}: {e}')
  return set(json_data.keys())

# Returns a set of unique urls that are already in urls.txt
def read_new_urls():
  try:
    # TODO: Use file access lock mechanism
    with open(input_file, 'r') as file:
      urls = {line.strip() for line in file if line.strip()}
  except IOError as e:
    print(f'Error reading {input_file}: {e}')
    urls = set()
  return urls

# Returns a queue of unique urls that are in urls.txt not in data.json (i.e. unprocessed urls)
def read_unprocessed_urls():
  processed_urls = read_processed_urls()
  new_urls = read_new_urls()
  unique_urls = new_urls - processed_urls
  unique_queue = queue.Queue()
  for url in unique_urls:
    unique_queue.put(url)
  print(f'Unique unprocessed urls: {list(unique_queue.queue)}')
  return unique_queue

def remove_trailing_slash_from_urls(new_urls):
  return [url.rstrip('/') for url in new_urls]

def remove_duplicate_urls(new_urls):
  return set(new_urls)

# Returns unique urls that are not in urls.txt and data.json
def remove_existing_urls(urls):
  processed_urls = read_processed_urls()
  new_urls = read_new_urls()
  return urls - processed_urls - new_urls

# Writes unique unprocessed urls to urls.txt
def write_urls(urls):
  print(f'Writing the following urls to {input_file}: {urls}')
  try:
    # TODO: Use file access lock mechanism
    with open(input_file, 'a') as file:
      for url in urls:
        file.write(f'{url}\n')
  except IOError as e:
    print(f'Error writing {output_file}: {e}')

# Write all the urls and extracted data to data.json
def write_data(new_data):
  try:
    # TODO: Use file access lock mechanism
    with open(output_file, 'r+') as file:
      try:
        # Read existing JSON data
        json_data = json.load(file)
      except json.JSONDecodeError:
        # If file is empty, initialize with empty JSON data
        json_data = {}
      
      # Append new data to existing/empty JSON data
      print(f'Writing the new data to {output_file}: {new_data}')
      json_data.update(new_data)
      
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
  
  urls = read_unprocessed_urls()
  
  # TODO: Incorporate multiprocessing here
  while not urls.empty():
    url = urls.get()
    print(f'Processing {url}...')
    
    # TODO: Crawl with the url and get back HTML content
    # TODO: Extract HTML content
    json_data, new_urls = {}, ['www.googles.com', 'www.apples.com']
    
    # Process new urls
    new_urls = remove_trailing_slash_from_urls(new_urls)
    # Assuming urls returned are not unique
    new_urls = remove_duplicate_urls(new_urls)
    # Remove urls that already exist in urls.txt
    new_unique_urls = remove_existing_urls(new_urls)
    
    # Write to files
    write_urls(new_unique_urls)
    write_data({url: {'html': json_data, 'urls': list(new_urls)}})
    