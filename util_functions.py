from bs4 import BeautifulSoup
import requests
import scraper_functions as scrape
import pandas as pd

# messages
def message():
    print("Welcome to RA Scraper (beta)")
    print("Scrape data on events, clubs, or artists and save the data as a CSV, JSON, or Excel file \n")
    print("Keywords are 'events', 'clubs', and 'artists'")
    print("For more information on these keywords, type 'help' \n")

def help_message():
    print("'events' will save data from the event pages of a given club/promoter")
    print("'clubs' will save data from the club pages of a given city")
    print("'artists' will save data from an artist page of a given artist name \n")

# keyword functions
def events(format,keyword):
    club = input("Name of club/promoter: ").lower()
    min_year = input("From what year?: ")
    max_year = input("Until what year?: ")
    years = [str(x) for x in range(int(min_year),int(max_year)+1)]
    club_url = search_club(club)
    print(f'Found club url {club_url}')
    results = scrape._events(club_url,club,years)
    save_results(results,club,format,keyword)

def clubs(format,keyword):
    city = input("Name of city: ").lower()
    city_url = search_city(city).replace('local','clubs')
    print(f'Found city url {city_url} \n')
    results = scrape._clubs(city_url,city)
    save_results(results,city,format,keyword)

# def artists(format):
#     artist_name = input("Name of artist: ").lower()
#     artist_url = search_artist(artist_name)

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
    club_link = soup.find('a',class_='f24').get('href')
    return club_link

# save function
def save_results(results,search_term,format,keyword):
    df = pd.DataFrame(results)

    if keyword == 'clubs':
        path = '/club_data/'
    elif keyword == 'events':
        path = '/data/'
    if format == 'excel':
        df.to_excel(f'{path}{search_term}.xlsx',header=df.columns,index=False)
        return print("Results saved")
    elif format == 'csv':
        df.to_csv(f'{path}{search_term}.csv',header=df.columns,index=False)
        return print("Results saved")
    elif format == 'json':
        df.to_json(f'{path}{search_term}.json',header=df.columns,index=False)
        return print("Results saved")
    else:
        print(f"Error format: '{format}' not valid \n Saving as CSV")
        df.to_csv(f'{search_term}.csv',header=df.columns,index=False)