# Resident Advisor Web Scraper
##### A web scraper designed to collect club & event details from Resident Advisor

Requirements:
+ Python 3.0+
+ Pandas
+ BeautifulSoup
+ tqdm

Given a keyword that describes the intent of the scrape (clubs or events), the application takes in a city or club/promoter name, and scrapes the data, and saves it into a specified file format. The default file format is CSV, but you can specify JSON or Excel if you'd like.

Keywords:
+ 'events'
   This will scrape the event calendars of a specific club/promoter. The prompt will ask for the name of the club/promoter and years you want to scrape.
+ 'clubs'
   This will scrape the club information of a city. The prompt will ask what city you would like to scrape.
