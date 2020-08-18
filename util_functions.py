import pandas as pd
import qri_pipeline as pipeline
from search import Search

# messages
def message():
    print('''
          Scrape data on events or clubs, and save the data as a CSV, JSON, or Excel file \n
          Keywords are 'events', 'clubs', and 'pipeline'
          For more information on these keywords, type 'help' \n
          ''')

def help_message():
    print('''
          'events' will save data from the event pages of a given club/promoter \n
          'clubs' will save data from the club pages of a given city \n
          'pipeline' starts scraping events for clubs already in the Qri dataset
          ''')

def prompt():
    return input("Keyword: ").lower()

def process(keyword,format):
    if keyword == 'events':
        Search(keyword,format).events()
    elif keyword == 'clubs':
        Search(keyword,format).clubs()
    elif keyword == 'pipeline':
        pipeline.run_pipeline()
    else:
        print('Error: keyword not recognized \n')
        keyword = prompt()
        process(keyword,format)

# save function
def save_results(
        results,search_term,format,
        keyword):
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
