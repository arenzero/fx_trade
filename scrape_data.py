# -*- coding: utf-8 -*-
from scraping.scrape_fx_data import scrape
import sys

def main():
    start = sys.argv[1]
    end = sys.argv[2]

    try:
        scrape(start=start,end=end)
        print('done')
    except BaseException as e:
        print(e)
        print('error')

if __name__ == "__main__":
    main()
    
