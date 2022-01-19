from bs4 import BeautifulSoup  # BS change HTML code to take information
from requests import get  # downloading code from web

import scrap_config

def float_parse(object):
    return float(object.replace(' ','').replace('zł', '').replace(',', '.').replace('m²', ''))

def int_parse(object):
    return int(object.replace(' ','').replace('zł', '').replace(',', '.').replace('m²', ''))


page = get(scrap_config.URL)
bs = BeautifulSoup(page.content, "html.parser")


for offer in bs.find_all('a', attrs={'data-cy':'listing-item-link'}):
    link = 'https://www.otodom.pl'+ offer['href']  # gettin link and addint otodom.pl
    title = offer.find('h3', attrs={'data-cy':'listing-item-title'}).get_text().strip()  # taking title from h3

    offer_page = get(link)
    offer_link = BeautifulSoup(offer_page.content, "html.parser")

    price = float_parse(offer_link.find('strong').get_text())
    print(price)
    area = float_parse(offer_link.find('div', attrs={'aria-label':'Powierzchnia'}).get_text().split(':')[1])
    price_per_sqm = round(price / area, 2)
    room = offer_link.find('div', attrs={'aria-label':'Liczba pokoi'}).get_text().split(':')[1]
    rent = offer_link.find('div', attrs={'aria-label':'Czynsz'}).get_text().split(':')[1]
    heat = offer_link.find('div', attrs={'aria-label':'Ogrzewanie'}).get_text().split(':')[1]

    print(title, price, area, price_per_sqm, room, rent, heat)
    break
