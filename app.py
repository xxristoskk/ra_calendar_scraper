import util_functions as util

def main():

    # boolean that keeps the scraper running
    running = True
    # welcome message
    util.message()

    while running:
        # prompt for the keyword
        keyword = util.prompt()
        if keyword == 'help':
            util.help_message()
            keyword = util.prompt()
        # choosing the format of save data
        save_format = input("Save data in which format?: ").lower()
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
