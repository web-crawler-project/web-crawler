import requests
import socket
import json
from bs4 import BeautifulSoup


def scrape_website(url):
    try:
        response = requests.get("http://"+ url)
        
        #Check if the request was successful
        if response.status_code == 200:
            time = response.elapsed.total_seconds()
            ip = socket.gethostbyname(url)
            geo = get_geolocation(ip)
            #Parse the HTML content of the page using BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')
            
            #Print the HTML content of the page for debug
            print(soup.prettify())
            print(f"Response time: {time}s")
            city = geo['city']
            country = geo['country_name']
            latitude = geo['latitude']
            longitude = geo['longitude']

            print(f"IP Address: {ip}\nCity: {city} \nCountry: {country}\nLatitude: {latitude}\nLongitude: {longitude}")
            return soup, time, ip, geo
            
            #Extract all the links in the page:
            #links = soup.find_all('a')
            #for link in links:
                #print("Link: ", link.get('href'))


        else:
            print("Failed to retrieve the web page. Status code:", response.status_code)

    except requests.exceptions.RequestException as e:
        print("Request Error:", e)
    #except Exception as e:
        #print("An error occurred:", e)

def get_geolocation(ip_address):
    url = 'https://geolocation-db.com/jsonp/' + ip_address
    response = requests.get(url)
    result = response.content.decode()
    result = result.split("(")[1].strip(")")
    data  = json.loads(result)
    return data

   

scrape_website("www.facebook.com")
