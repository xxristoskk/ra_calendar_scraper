import requests
from bs4 import BeautifulSoup
import util_functions as util
from scraper import Scrape
import qri_pipeline as pipeline

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
        if pipeline.check('club', club):
            club_url = pipeline.find_url(club)
        else:
            club_url = search_club(club)
        print(f'Found club url {club_url}')
        results = Scrape(club_url).events(club,years)
        util.save_results(
            results,club,
            self.format,self.key
        )

    def clubs(self):
        city = input("Name of city: ").lower()
        if pipeline.check('city', city):
            print("City already scraped! Choose another.")
            city = input("Name of city: ").lower()
        city_url = search_city(city).replace('local','clubs')
        print(f'Found city url {city_url} \n')
        results = Scrape(city_url).clubs(city)
        util.save_results(
            results,city,
            self.format,self.key
        )

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
