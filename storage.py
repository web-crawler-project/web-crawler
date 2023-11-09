import json
import re
import os


def remove_trailing_slash_from_urls(new_urls):
    return [url.rstrip('/') for url in new_urls]


def remove_duplicate_urls(new_urls):
    return set(new_urls)


# Returns a set of unique urls that are already in urls.txt
def read_seed_urls(seed_file):
    try:
        with open(seed_file, 'r') as file:
            urls = [line.strip() for line in file if line.strip()]
    except IOError as e:
        pass
        urls = set()
    return urls


# Returns a set of unique urls that are already in data.json
def read_processed_urls(output_file):
    json_data = {}
    try:
        with open(output_file, 'r') as file:
            try:
                # Read existing JSON data
                json_data = json.load(file)
            except json.JSONDecodeError:
                pass
    except IOError as e:
        pass
    return set(json_data.keys())


# Returns unique urls that are not in urls.txt and data.json
def remove_existing_urls(urls, output_file):
    processed_urls = read_processed_urls(output_file)
    return urls - processed_urls


# Write all the urls and extracted data to data.json
def write_data(url, new_data, output_file):
    try:
        with open(output_file, 'r+') as file:
            try:
                # Read existing JSON data
                json_data = json.load(file)
            except json.JSONDecodeError:
                # If file is empty, initialize with empty JSON data
                json_data = {}

            # Append new data to existing/empty JSON data
            json_data.update({url: new_data})

            # Write updated JSON data to file
            file.seek(0)
            json.dump(json_data, file, indent=2)
            file.truncate()
    except IOError as e:
        print(f'Error writing {output_file}: {e}')

# Remove urls which were searched before
def remove_seen_urls(queue, new_urls, output_file):
    # Process new urls
    new_urls = remove_trailing_slash_from_urls(new_urls)
    new_urls = remove_duplicate_urls(new_urls)
    # Remove urls that have already been crawled
    new_unique_urls = remove_existing_urls(new_urls, output_file)
    # Remove urls that are already in queue
    set_queue = set(queue)
    return list(set_queue.union(new_unique_urls) - set_queue)

# Read list of keywords from file path
def read_keywords(keyword_file):
    keywords = set()
    try:
        with open(keyword_file, 'r') as file:
            for line in file:
                # Convert to lower case
                split_line = line.lower().split()
                for word in split_line:
                    # Remove all non-alphanumeric characters
                    replace_word = re.sub(r'\W+', '', word)
                    if replace_word not in keywords:
                        keywords.add(replace_word)

    except IOError as e:
        print(f'Error reading {keyword_file}: {e}')
    return keywords

# Create a blank JSON output file with specified output path
def initialize_output_file(output_file):
    try:

        # Create directory if it does not exist
        directory = os.path.dirname(output_file)
        if not os.path.exists(directory):
            os.makedirs(directory)

        # Create a empty file
        with open(output_file, 'w') as file:
            file.write('')
    except IOError as e:
        print(f'Error writing {output_file}: {e}')
