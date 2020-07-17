from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import requests
from datetime import timedelta,date
import time
import re
from tqdm import tqdm

def ra_scraper(url,club):
    years = ['2015','2016','2017','2018','2019','2020']
    events = []
    for year in tqdm(years):
        print(f'Scraping year {year}')
        r = requests.get(f"https://www.residentadvisor.net{url}&show=events&yr={year}")
        soup = BeautifulSoup(r.text, 'html.parser')
        articles = soup.find_all('article')
        print(f'Found {len(articles)} events')
        for article in articles:
            article_number = len(articles) - articles.index(article)
            print(f'Event {article_number} of {len(articles)}')
            event_dict = {}
            try:
                event_dict['date'] = article.find('p',class_='date').get_text()
            except:
                event_dict['date'] = article.find('p',class_='flag').get_text()
            event_dict['link'] = article.find('a').get('href')
            event_dict['name'] = article.find('h1').get_text()
            event_dict['lineup'] = get_lineup(event_dict['link'],club)
            print('Added:'+'\n'+event_dict['date']+'\n'+event_dict['name']+'\n'+str(event_dict['lineup'])+'\n')
            events.append(event_dict)
        time.sleep(2)
    return events

def get_lineup(link, club):
    r = requests.get(f"https://www.residentadvisor.net{link}")
    soup = BeautifulSoup(r.text, 'html.parser')
    if soup.find('p',class_='lineup medium') == None:
        try:
            box_lineup = soup.find('p',class_='lineup large')
            lineup = re.sub(f"{club.capitalize()}:",'',box_lineup.get_text()).split("\n")
        except:
            box_lineup = soup.find('p',class_='lineup small')
            lineup = re.sub(f"{club.capitalize()}:",'',box_lineup.get_text()).split("\n")
    else:
        box_lineup = soup.find('p',class_='lineup medium')
        lineup = re.sub(f"{club.capitalize()}:",'',box_lineup.get_text()).split("\n")
    if club.capitalize() in lineup:
        lineup = [x for x in lineup if x != club.capitalize()]
    time.sleep(1)
    return [x for x in lineup if x != '']

def search_club(club):
    search_url = f'https://www.residentadvisor.net/search.aspx?searchstr={club}'
    r = requests.get(search_url)
    soup = BeautifulSoup(r.text, 'html.parser')
    club_link = soup.find('a',class_='f24').get('href')
    return club_link

def save_results(results,club):
    df = pd.DataFrame(results)
    df['date'] = pd.to_datetime(df['date'])
    df.to_excel(f'{club}.xlsx',header=df.columns,index=False)
    return

def main():

    running = True
    while running:

        club = input("Name of club: ").lower()
        club_url = search_club(club)
        print(f'Found club url {club_url}')
        results = ra_scraper(club_url,club)
        save_results(results,club)

        print("Results saved")
        exit_prompt = input("Scrape another club?(y/n): ")
        if exit_prompt == 'n':
            running = False
        else:
            continue

if __name__ == '__main__':
    main()
