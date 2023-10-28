import concurrent.futures
import threading
from time import sleep
from scraper import scrape_website
from html_extractor import extract_html
from storage import write_data, remove_seen_urls, read_seed_urls


def task(queue, output_file):
    with mutex:
        url = queue.pop(0)
        print(f"Trying {url}...")
    for i in range(5):
        try:
            soup, time, ip, geo = scrape_website(url)
            extracted_data, new_urls = extract_html(soup)
            data_to_write = {'ip': ip, 'geolocation': geo, 'response_time': time, 'data': extracted_data}
            with mutex:
                unseen_urls = remove_seen_urls(queue, new_urls, output_file)
                data_to_write['new_urls'] = unseen_urls
                queue.extend(unseen_urls)
                write_data(url, data_to_write, output_file)
                print(f'Finished processing {url}...')
            break
        except:
            sleep(0.1)

def main():
    # To limit the number of tasks executed
    limit = 100
    num_submitted = 0

    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Submit the first batch of tasks
        futures = [executor.submit(task, queue, output_file) for i in range(len(queue))]
        num_submitted += len(queue)

        # Monitor completion of tasks
        while futures:
            done, _ = concurrent.futures.wait(futures, return_when=concurrent.futures.FIRST_COMPLETED)

            for future in done:
                futures.remove(future)

                if (num_submitted == limit):
                    break

                # Submit a new task if available
                for i in range(len(queue)):
                    futures.append(executor.submit(task, queue, output_file))
                    num_submitted += 1

                    if (num_submitted == limit):
                        break
                    sleep(0.1)


if __name__ == "__main__":
    mutex = threading.Lock()
    seed_file = 'urls.txt'
    output_file = 'data.json'
    queue = read_seed_urls(seed_file)
    main()