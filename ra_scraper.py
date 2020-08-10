import util_functions as f

def main():

    # boolean that keeps the scraper running
    running = True
    # welcome message
    f.message()

    while running:
        # prompt for the keyword
        keyword = f.prompt()

        if keyword == 'help':
            f.help_message()
            keyword = f.prompt()

        # choosing the format of save data
        save_format = input("Save data in which format?: ").lower()
        # processing the keyword
        f.process(keyword,save_format)

        # prompt for continuing or breaking the while loop
        exit_prompt = input("Scrape again?(y/n): ")
        if exit_prompt == 'n':
            running = False
        else:
            continue

if __name__ == '__main__':
    main()
