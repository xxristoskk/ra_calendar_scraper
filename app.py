import util_functions as util

def main():

    # boolean that keeps the scraper running
    running = True
    # welcome message
    print('''
          Scrape data on events or clubs, and save the data as a CSV, JSON, or Excel file \n
          Keywords are 'events', 'clubs', and 'pipeline'
          For more information on these keywords, type 'help' \n
          ''')

    while running:
        # prompt for the keyword
        keyword, save_format = util.prompt()
        # processing the keyword
        util.process(keyword,save_format)
        # prompt for continuing or breaking the while loop
        exit_prompt = input("Scrape again?(y/n): ")
        if exit_prompt == 'n':
            running = False
        else:
            continue

if __name__ == '__main__':
    main()
