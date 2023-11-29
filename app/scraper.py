import httpx
from bs4 import BeautifulSoup as bs
from .db_function import save_db
from .models import Items, Requests
import datetime

header = {
    "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/119.0.0.0'
                  'Safari/537.36'}


############################ EMAG ##################################

# search in html page where price is by class name and html tag
def search_price(doc):
    price_html = doc.find_all('p', {'class': 'product-new-price'})[0].text
    price = f'{price_html}'.replace(',', '.').strip(' Lei').split('.')
    cents = price.pop()
    full_price = f'{"".join(price)}.{cents}'
    return full_price


# get html page based on link
def get_doc(link):
    result = httpx.get(link.link, timeout=None, headers=header)
    doc = bs(result.text, 'html.parser')
    return doc


# save title and price in db
def save_link(link):
    doc = get_doc(link)

    product_name = doc.title.text
    full_price = search_price(doc)

    items = Items(title=product_name, price=float(full_price), link_id=link.id)
    save_db(items)
    return items


# save request done
def save_request(link):
    doc = get_doc(link)

    full_price = search_price(doc)
    request_date = datetime.datetime.today()

    request = Requests(request_data=request_date, request_price=float(full_price), product_id=link.id)
    save_db(request)
    return request


############################ ALTEX ##################################
"""
def search(doc):
    price = doc.find_all('span', {'class': 'Price-int leading-none'})[1].text
    cents = doc.find_all('sup', {'class': 'inline-block -tracking-0.33'})[1].text
    full_price = f'{price}{cents}'.replace(',', '.')
    return full_price

class Scrapper:

    @staticmethod
    def save_link(link):
        result = httpx.get(link, timeout=None, headers=headers)
        doc = bs(result.text, 'html.parser')
    
        product_name = doc.title.text
        full_price = search(doc)
        date = datetime.today()
    
        items = Items(title=product_name, price=float(full_price), link_id=link.id)
        save_database(items)
        return items
    
    @staticmethod
    def make_request(link):
        result = httpx.get(link.link, timeout=None, headers=headers)
        doc = bs(result.text, 'html.parser')
    
        full_price = search(doc)
        request_date = datetime.today()
    
        request = Requests(request_data=request_date, request_price=float(full_price), product_id=link.id)
        save_database(request)
        return request
    """

############################ AMAZON ##################################
"""
def search(doc):
    price = doc.find_all('span', {'class': 'Price-int leading-none'})[1].text
    cents = doc.find_all('sup', {'class': 'inline-block -tracking-0.33'})[1].text
    full_price = f'{price}{cents}'.replace(',', '.')
    return full_price

class Scrapper:

    @staticmethod
    def save_link(link):
        result = httpx.get(link, timeout=None, headers=headers)
        doc = bs(result.text, 'html.parser')

        product_name = doc.title.text
        full_price = search(doc)
        date = datetime.today()

        items = Items(title=product_name, price=float(full_price), link_id=link.id)
        save_database(items)
        return items

    @staticmethod
    def make_request(link):
        result = httpx.get(link.link, timeout=None, headers=headers)
        doc = bs(result.text, 'html.parser')

        full_price = search(doc)
        request_date = datetime.today()

        request = Requests(request_data=request_date, request_price=float(full_price), product_id=link.id)
        save_database(request)
        return request
    """