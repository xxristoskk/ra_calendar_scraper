import qri_ra_events_pipeline as pipeline
import requests
from bs4 import BeautifulSoup
import util_functions as f
import scraper_functions as scrape

class Search():
    def __init__(self,key,format):
        self.key = key
        self.format = format

    # keyword functions
    def events(self):
        club = input("Name of club/promoter: ").lower()
        min_year = input("From what year?: ")
        max_year = input("Until what year?: ")
        years = [str(x) for x in range(int(min_year),int(max_year)+1)]
        if check_pipeline():
            club_url = pipeline.find_url(self.key)
        else:
            club_url = search_club(self.key)
        print(f'Found club url {club_url}')
        results = scrape._events(club_url,club,years)
        f.save_results(results,club,self.format,self.key)

    def clubs(self):
        city = input("Name of city: ").lower()
        city_url = search_city(city).replace('local','clubs')
        print(f'Found city url {city_url} \n')
        results = scrape._clubs(city_url,city)
        f.save_results(results,city,self.format,self.key)

# search functions
def search_city(city):
    search_url = f'https://www.residentadvisor.net/search.aspx?searchstr={city}'
    r = requests.get(search_url)
    soup = BeautifulSoup(r.text,'html.parser')
    try:
        link_holder = soup.find('li',class_='clearfix')
        city_link = link_holder.find('a').get('href')
    except:
        link_holder = soup.find('div',class_='but heading-more mobile-off')
        city_link = link_holder.find('a').get('href')
    return city_link.replace('events','clubs')

def search_club(club):
    search_url = f'https://www.residentadvisor.net/search.aspx?searchstr={club}'
    r = requests.get(search_url)
    soup = BeautifulSoup(r.text, 'html.parser')
    try:
        club_link = soup.find('a',class_='f24').get('href')
    except:
        club_link = soup.find('ul',class_='list').find('a').get('href')
    return club_link
