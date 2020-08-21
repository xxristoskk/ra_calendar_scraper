import pandas as pd
import qri_pipeline as pipeline
from search import Search

def help_message():
    print('''
          'events' will save data from the event pages of a given club/promoter \n
          'clubs' will save data from the club pages of a given city \n
          'pipeline' starts scraping events for clubs already in the Qri dataset
          ''')

def prompt():
    keyword = input("Keyword: ").lower()
    if keyword == 'help':
        help_message()
        keyword, save_format = prompt()
    save_format = input("Save data in which format?: ").lower()
    return keyword, save_format

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
