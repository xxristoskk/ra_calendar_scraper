from bs4 import BeautifulSoup
import requests
import time
import re
from tqdm import tqdm
import qri

df = qri.get("xristosk/ra_event_info").body
event_ids = list(df['event_id'])

class Scrape():
    def __init__(self,url):
        self.url = url

    def artists(self,name_list):
        artists = []
        for artist in tqdm(name_list):
            time.sleep(2)
            print('\n')
            print(f"Scraping {artist[0]} ({name_list.index(artist)} of {len(name_list)})... \n")
            r = requests.get(f'{self.url}{artist[1]}')
            soup = BeautifulSoup(r.text, 'html.parser')
            header = soup.find('ul',class_='clearfix')
            if header.find('div', class_='fl'):
                country = header.find('span').get_text().strip('\xa0 ').lower()
            else:
                country = -1
            sections = soup.find_all('div', class_='pr8')
            for section in sections:
                if section.find('h1'):
                    if 'statistics' in section.find('h1').get_text():
                        event_soup = section.find_all('article', class_='highlight-top')
                    elif 'Labels' in section.find('h1').get_text():
                        label_soup = section.find_all('article', class_='highlight-top')
                else:
                    continue
            if len(event_soup) < 3:
                clubs = -1
            else:
                labels = [x.find('h1').get_text().lower() for x in label_soup if x.find('h1').get_text() != '']
                clubs = [x.get_text().lower() for x in event_soup[2].find_all('a') if x.get_text() != '']
                regions = [x.get_text().lower() for x in event_soup[1].find_all('a') if x.get_text() != '']
            artist_dict = {
                'artist_name': artist[0],
                'country': country,
                'ra_followers': soup.find('h1', class_='favCount').get_text().strip('\n'),
                'labels': [x.find('h1').get_text().lower() for x in label_soup],
                'most_played_clubs': clubs,
                'most_played_regions': [x.strip('\n') for x in regions],
                'appears_with': [x.get_text().lower() for x in event_soup[0].find_all('a')],
            }
            print(artist_dict)
            artists.append(artist_dict)
            print('\n')
        return artists


    def clubs(self,city):
        clubs = get_clubs(self.url)
        club_list = []
        for club in tqdm(clubs):
            print('\n')
            # set default capacity to -1
            club_dict = {'capacity': -1}
            club_url = club['url']
            r = requests.get(f'https://www.residentadvisor.net{club_url}')
            soup = BeautifulSoup(r.text,'html.parser')
            section = soup.find('ul', class_='clearfix')
            club_dict = {
                'club_name': club['name'],
                'club_id': club_url.replace("/club.aspx?id=",'').strip(''),
                'address': club['address'],
                'city': city
            }
            # not all pages have country
            try:
                club_dict['country'] = section.find('div', class_='fl').get_text()
            except:
                club_dict['country'] = ''
            # looking for Capacity of club
            li_list = section.find_all('li')
            for li in li_list:
                if 'Capacity' in li.get_text():
                    club_dict['capacity'] = li.get_text().split('/')[1]
            print(f'{club_dict} \n')
            club_list.append(club_dict)
            time.sleep(2)
        return club_list

    def events(self,club,years):
        events = []
        for year in tqdm(years):
            print(f'Scraping year {year}')
            r = requests.get(f"https://www.residentadvisor.net{self.url}&show=events&yr={year}")
            soup = BeautifulSoup(r.text, 'html.parser')
            articles = soup.find_all('article')
            print(f'Found {len(articles)} events')
            for article in articles:
                article_number = articles.index(article) + 1
                if article.find('a').get('href').replace('/events/','') in event_ids:
                    continue
                print(f'Event {article_number} of {len(articles)}')
                event_dict = {
                    'link': article.find('a').get('href'),
                    'name': article.find('h1').get_text(),
                }
                event_dict['lineup'] = get_lineup(event_dict['link'],club)
                try:
                    event_dict['date'] = article.find('p',class_='date').get_text()
                except:
                    event_dict['date'] = article.find('p',class_='flag').get_text()
                print('Added:'+'\n'+event_dict['date']+'\n'+event_dict['name']+'\n'+str(event_dict['lineup'])+'\n')
                events.append(event_dict)
            time.sleep(2)
        return events

def get_clubs(url):
    r = requests.get(f'https://www.residentadvisor.net{url}')
    soup = BeautifulSoup(r.text, 'html.parser')
    club_items = soup.find_all('div',class_='fl')
    clubs = []
    for i in range(1,len(club_items),2):
        if club_items[i].find('a') != None:
            club = {
                'name': club_items[i].get_text(),
                'address': club_items[i+1].get_text(),
                'url': club_items[i].find('a').get('href')
            }
            clubs.append(club)
        elif club_items[i].find('a') == None:
            break
    return clubs

def get_lineup(url, club):
    r = requests.get(f"https://www.residentadvisor.net{url}")
    soup = BeautifulSoup(r.text, 'html.parser')
    ## looks for lineup on page in 3 different classes
    if soup.find('p',class_='lineup medium') == None:
        try:
            box_lineup = soup.find('p',class_='lineup large')
            #removes club name from lineup
            lineup = re.sub(f"{club.capitalize()}:",'',box_lineup.get_text()).split("\n")
        except:
            box_lineup = soup.find('p',class_='lineup small')
            lineup = re.sub(f"{club.capitalize()}:",'',box_lineup.get_text()).split("\n")
    else:
        try:
            box_lineup = soup.find('p',class_='lineup medium')
            lineup = re.sub(f"{club.capitalize()}:",'',box_lineup.get_text()).split("\n")
            if club.capitalize() in lineup:
                lineup = [x for x in lineup if x != club.capitalize()]
        except:
            print('No lineup found')
    time.sleep(2)
    return [x for x in lineup if x != ''] #returning lineup list without any empty strings
