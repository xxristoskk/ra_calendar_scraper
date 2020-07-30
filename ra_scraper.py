from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import requests
from datetime import timedelta,date
import time
import re
from tqdm import tqdm
import util_functions as f

def process(keyword,format):
    if keyword == 'events':
        return f.events(format,keyword)
    elif keyword == 'clubs':
        return f.clubs(format,keyword)
    elif keyword == 'artist':
        print("This function is not available yet.")
        return False
    elif keyword == 'help':
        f.help_message()
        return False

def main():

    running = True
    f.message()

    while running:

        save_format = input("Save data in which format?: ").lower()
        keyword = input("Searching for events, clubs, or artist?: ").lower()

        if not process(keyword,save_format):
            keyword = input("Searching for events, club, or artist?: ").lower()
            process(keyword,save_format)

        exit_prompt = input("Scrape again?(y/n): ")

        if exit_prompt == 'n':
            running = False
        else:
            continue

if __name__ == '__main__':
    main()
