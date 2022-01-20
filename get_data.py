from bs4 import BeautifulSoup  # BS change HTML code to take information
from requests import get  # downloading code from web

import scrap_config
import send_to_pg
import is_new

def float_parse(object):
    clean_object = object.replace(' ','').replace('zł', '').replace(',', '.').replace('m²', '')
    try:
        return float(clean_object)
    except:
        return clean_object

def int_parse(object):
    return int(object.replace(' ','').replace('zł', '').replace(',', '.').replace('m²', ''))


def get_data():

    page = get(scrap_config.URL)
    bs = BeautifulSoup(page.content, "html.parser")


    for offer in bs.find_all('a', attrs={'data-cy':'listing-item-link'}):
        new_offer = None  # reset for new offers indicator

        link = 'https://www.otodom.pl'+ offer['href']  # gettin link and addint otodom.pl
        title = offer.find('h3', attrs={'data-cy':'listing-item-title'}).get_text().strip()  # taking title from h3

        offer_page = get(link)
        offer_link = BeautifulSoup(offer_page.content, "html.parser")
        try:
            localization = offer_link.find('a', attrs={'aria-label':'Adres'}).get_text()
            price = float_parse(offer_link.find('strong').get_text())
            area = float_parse(offer_link.find('div', attrs={'aria-label':'Powierzchnia'}).get_text().split(':')[1])
            price_per_sqm = round(price / area, 2)
            room = offer_link.find('div', attrs={'aria-label':'Liczba pokoi'}).get_text().split(':')[1]
            try:
                rent = float_parse(offer_link.find('div', attrs={'aria-label':'Czynsz'}).get_text().split(':')[1])
            except:
                rent = "Brak danych"

            try:
                heat = offer_link.find('div', attrs={'aria-label':'Ogrzewanie'}).get_text().split(':')[1]
            except:
                heat = "Brak danych"

            floor = offer_link.find('div', attrs={'aria-label':'Piętro'}).get_text().split(':')[1]

            print(link, title, localization, price, area, price_per_sqm, room, rent, heat, floor)

            new_offer = is_new.new_offer(link)  #checking if the offer is in the base 0 new 1 mean old
            if new_offer == 0:
                send_to_pg.send(link, title, localization, price, area, price_per_sqm, room, rent, heat, floor)
                print("Offer send to database")
            else:
                print("Offer is already in database")
        except:
            print("Offer got an error")