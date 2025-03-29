import cloudscraper
from bs4 import BeautifulSoup

def getHTML(url) -> BeautifulSoup:
    scraper = cloudscraper.create_scraper()
    page = scraper.get(url).content

    return BeautifulSoup(page, 'html.parser')

def parser():
    count = 10
    while count > 0:
        print("Count " + str(11 - count))
        html = getHTML("https://yandex.ru/pogoda/month")
        first_row = html.select_one(".climate-calendar__row:not(.climate-calendar__row_header)")
        if first_row is not None:
            break
        count -= 1
    
    if first_row is not None:
        first_col = first_row.select_one(".climate-calendar__cell")
        cell = first_col.select_one(".a11y-hidden")

        print(cell.text)
    else:
        print("ERROR: Can not parse this page")
        
parser()