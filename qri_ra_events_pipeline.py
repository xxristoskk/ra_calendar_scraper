import pandas as pd
from tqdm import tqdm
import time
from scraper_functions import Scrape
import util_functions as f
import os
import qri

club_df = qri.get('xristosk/ra_club_info').body
folder = '/home/xristos/projects/ra_calendar_scraper/data'

# creates a list of clubs that have already been scraped
already_scraped = []
for name in os.listdir(folder):
    if '.xlsx' in name:
        already_scraped.append(name.split('.xlsx')[0].strip())
    elif '.csv' in name:
        already_scraped.append(name.split('.csv')[0].strip())

def run_pipeline():
    key = input("Scrape events in which city?: ").lower()
    for i,row in tqdm(club_df[club_df['city']==key].iterrows()):
        club_name = row['club_name'].split('/')[0].strip() # any venue that is split into parts is named by the first part
        if club_name in already_scraped:
            continue
        else:
            city = row['city']
            club_id = row['club_id']
            years = [str(x) for x in range(2015,2021)]
            print(f'Scraping {club_name} in {city} \n')
            time.sleep(2)
            results = Scrape(f'/club.aspx?id={club_id}').events(club_name,years)
            f.save_results(results,club_name,'csv','events')

def find_url(club):
    club_id = club_df[club_df['club_name']==club]['club_id']
    return f'/club.aspx?id={club_id}'
