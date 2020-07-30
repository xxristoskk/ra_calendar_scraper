from bs4 import BeautifulSoup
import requests
import time
import re
from tqdm import tqdm

def _clubs(url,city):
    clubs = get_clubs(url)
    club_list = []
    for club in tqdm(clubs):
        print(club)
        time.sleep(2)
        club_dict = {'capacity': -1}
        url = club[0]
        r = requests.get(f'https://www.residentadvisor.net{url}')
        soup = BeautifulSoup(r.text,'html.parser')
        section = soup.find('ul',class_='clearfix')
        club_dict['club_name'] = club[1]
        club_dict['club_id'] = url.replace("/club.aspx?id=",'').strip('')
        club_dict['address'] = club[2]
        club_dict['country'] = section.find('div',class_='fl').get_text()
        club_dict['city'] = city
        li_list = section.find_all('li')
        for li in li_list:
            if 'Capacity' in li.get_text():
                club_dict['capacity'] = li.get_text().split('/')[1]
        print(club_dict)
        club_list.append(club_dict)
    return club_list

def _events(url,club,years):
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
            event_dict['lineup'] = f.get_lineup(event_dict['link'],club)
            print('Added:'+'\n'+event_dict['date']+'\n'+event_dict['name']+'\n'+str(event_dict['lineup'])+'\n')
            events.append(event_dict)
        time.sleep(2)
    return events

def get_clubs(url):
    r = requests.get(f'https://www.residentadvisor.net{url}')
    soup = BeautifulSoup(r.text, 'html.parser')
    club_items = soup.find_all('div',class_='fl')
    names = []
    addresses = []
    hrefs = []
    for i in range(1,len(club_items),2):
        if club_items[i].find('a') != None:
            print(club_items[i].find('a').get('href'))
            print(club_items[i].get_text())
            print(club_items[i+1].get_text() + '\n')
            names.append(club_items[i].get_text())
            addresses.append(club_items[i+1].get_text())
            hrefs.append(club_items[i].find('a').get('href'))
        elif club_items[i].find('a') == None:
            break
    # links = link_section.find_all('a')
    # names = [x.get_text() for x in links]
    # hrefs = [x.get('href') for x in links]
    return zip(hrefs,names,addresses)

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