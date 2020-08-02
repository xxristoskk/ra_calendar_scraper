import pandas as pd
from tqdm import tqdm
import time
import scraper_functions as scrape
import util_functions as f
import os
import qri

club_df = qri.get('xristosk/ra_club_info').body
folder = '/home/xristos/projects/ra_calendar_scraper/data'

already_scraped = []
for name in os.listdir(folder):
    if '.xlsx' in name:
        already_scraped.append(name.split('.xlsx')[0].strip())
    elif '.csv' in name:
        already_scraped.append(name.split('.csv')[0].strip())

def run_pipeline():
    for i,row in tqdm(club_df.iterrows()):
        if row['club_name'] in already_scraped:
            continue
        else:
            club_name = row['club_name']
            city = row['city']
            club_id = row['club_id']
            years = [str(x) for x in range(2015,2021)]
            print(f'Scraping {club_name} in {city} \n')
            time.sleep(2)
            results = scrape._events(f'/club.aspx?id={club_id}',club_name,years)
            save_results(results,row['club_name'],'csv','events')

def find_url(club):
    club_id = club_df[club_df['club_name']==club]['club_id']
    return f'/club.aspx?id={club_id}'
