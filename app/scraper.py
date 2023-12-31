from .db_function import save_db
from .models import Items, Requests, Products
from .db_function import paginate_db
from .initialize import scheduler

import httpx
from bs4 import BeautifulSoup as bs
import datetime

header = {
    "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/119.0.0.0'
                  'Safari/537.36'}


############################ EMAG ##################################


# get html page based on link
def get_doc(link):
    result = httpx.get(link.link, timeout=None, headers=header)
    doc = bs(result.text, 'html.parser')
    return doc


# search in html page where price is
def search_for_price(doc):

    price_html = doc.find_all('p', {'class': 'product-new-price'})[0].text
    price = f'{price_html}'.replace(',', '.').strip(' Lei').split('.')
    cents = price.pop()

    full_price = f'{"".join(price)}.{cents}'
    return full_price


# save title and price in db
def save_link(link):
    doc = get_doc(link)

    product_name = doc.title.text
    full_price = search_for_price(doc)

    items = Items(title=product_name, price=float(full_price), link_id=link.id)
    save_db(items)
    return items


# save the request in db
def save_request(link):
    doc = get_doc(link)

    full_price = search_for_price(doc)
    request_date = datetime.datetime.today()

    request = Requests(request_data=request_date, request_price=float(full_price), product_id=link.id)
    save_db(request)
    return request


# automatically create requests in every Sunday and save it
@scheduler.task('cron', id='create_request', week="*", day_of_week='sun')
def create_request():
    print('This task is created on every Sunday')
    with scheduler.app.app_context():
        links = paginate_db(Products)
        for link in links:
            save_request(link)
    return ''




##################################################################################################################

# @scheduler.task('interval', id='create_request', seconds=60)

                            ### AMAZON ###

# future plan for more shops