import concurrent.futures
import datetime
import threading
from time import sleep
from scraper import scrape_website
from html_extractor import extract_html
from storage import write_data, remove_seen_urls, read_seed_urls, read_keywords, initialize_output_file

# Task to be executed by each worker thread
def task(queue, output_file, keywords):
    # Get a url from the queue
    with mutex:
        url = queue.pop(0)
        print(f"Trying {url}...")

    # Tries to scrape the webpage 5 times, else carry on
    for i in range(5):
        try:
            soup, time, ip, geo = scrape_website(url)
            extracted_data, new_urls = extract_html(soup, keywords)

            if not extracted_data and not new_urls:
                print(f'Finished processing {url}, nothing interesting found...')
                break

            data_to_write = {'ip': ip, 'geolocation': geo, 'response_time': time, 'data': extracted_data}
            with mutex:
                unseen_urls = remove_seen_urls(queue, new_urls, output_file)
                queue.extend(unseen_urls)
                write_data(url, data_to_write, output_file)
                print(f'Data from {url} has been written to the output file...')
            break
        except:
            sleep(0.1)


def main():
    # To limit the number of tasks executed
    limit = 10000 # Change this to vary the number of pages to crawl
    num_submitted = 0

    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Submit the first batch of tasks
        futures = [executor.submit(task, queue, output_file, keywords) for i in range(len(queue))]
        num_submitted += len(queue)

        # Monitor completion of tasks
        while futures:
            done, _ = concurrent.futures.wait(futures, return_when=concurrent.futures.FIRST_COMPLETED)

            for future in done:
                futures.remove(future)

                if num_submitted == limit:
                    break

                # Submit new tasks if available
                for i in range(len(queue)):
                    futures.append(executor.submit(task, queue, output_file, keywords))
                    num_submitted += 1

                    if num_submitted == limit:
                        break


if __name__ == "__main__":
    current_datetime = datetime.datetime.now()
    formatted_datetime = current_datetime.strftime("%Y-%m-%d_%H-%M-%S")
    output_file = 'output/' + formatted_datetime + '.json'
    initialize_output_file(output_file)

    mutex = threading.Lock()
    seed_file = 'input/urls.txt'
    keywords_file = 'input/keywords.txt'
    output_file = output_file
    queue = read_seed_urls(seed_file)
    keywords = read_keywords(keywords_file)
    main()
