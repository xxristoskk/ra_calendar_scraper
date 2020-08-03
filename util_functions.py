from bs4 import BeautifulSoup
import requests
import scraper_functions as scrape
import pandas as pd
import qri
import qri_ra_events_pipeline as pipeline

# messages
def message():
    print("Scrape data on events or clubs, and save the data as a CSV, JSON, or Excel file \n")
    print("Keywords are 'events', 'clubs', and 'pipeline'")
    print("For more information on these keywords, type 'help' \n")

def help_message():
    print("'events' will save data from the event pages of a given club/promoter")
    print("'clubs' will save data from the club pages of a given city")
    print("'pipeline' starts scraping events for clubs already on Qri")
    # print("'artists' will save data from an artist page of a given artist name \n")

def prompt():
    return input("Searching for events, clubs, or pipeline?: ").lower()

def process(keyword,format):
    if keyword == 'events':
        events(format,keyword)
    elif keyword == 'clubs':
        clubs(format,keyword)
    elif keyword == 'pipeline':
        pipeline.run_pipeline()
    else:
        print('Error: keyword not recognized \n')
        keyword = prompt()
        process(keyword,format)

# creating functions to search through the qri pipeline as opposed to making requests to RA
def check_pipeline(club):
    if club in list(pipeline.club_df['club_names']):
        return True
    else:
        return False

# keyword functions
def events(format,keyword):
    club = input("Name of club/promoter: ").lower()
    min_year = input("From what year?: ")
    max_year = input("Until what year?: ")
    years = [str(x) for x in range(int(min_year),int(max_year)+1)]
    if check_pipeline():
        club_url = pipeline.find_url(club)
    else:
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


# save function
def save_results(results,search_term,format,keyword):
    df = pd.DataFrame(results)

    # if clubs were scraped it gets sent to this folder
    if keyword == 'clubs':
        path = 'club_data/'
    # if events were scraped it gets sent to this folder
    elif keyword == 'events' or path == 'pipeline':
        path = 'data/'
        
    if format == 'excel':
        df.to_excel(f'~/projects/ra_calendar_scraper/{path}{search_term}.xlsx',header=df.columns,index=False)
        return print("Results saved")
    elif format == 'csv':
        df.to_csv(f'~/projects/ra_calendar_scraper/{path}{search_term}.csv',header=df.columns,index=False)
        return print("Results saved")
    elif format == 'json':
        df.to_json(f'~/projects/ra_calendar_scraper/{path}{search_term}.json',header=df.columns,index=False)
        return print("Results saved")
    else:
        print(f"Error format: '{format}' not valid \n Saving as CSV")
        df.to_csv(f'~/projects/ra_calendar_scraper/{path}{search_term}.csv',header=df.columns,index=False)
