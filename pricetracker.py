#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup
import unicodedata

from send_email import send_email

AVAIL_VAL = '#availability .a-color-success'

HEADERS = ({'User-Agent':
            'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
            'Accept-Language': 'en-US, en;q=0.5'})


def get_product_info(url):
    page = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(page.content, features="lxml")

    try:
        title = soup.find(id='productTitle').get_text().strip()
        price_str = soup.find(class_='a-price-whole').get_text()
    except:
        return None, None, None

    try:
        soup.select(AVAIL_VAL)[0].get_text().strip()
        available = True
    except:
        available = False

    try:
        price = unicodedata.normalize('NFKD', price_str)
        price = price.replace('$', '').replace(',', '.')
        price = float(price)
    except:
        return None, None, None

    return title, price, available


if __name__ == '__main__':
    url = 'https://www.amazon.com/Fitbit-Fitness-Activity-Tracking-Included/dp/B084CQ41M2/ref=sr_1_3?crid=QAW2P53U5P42&keywords=fitbit+charge+4&qid=1643568553&sprefix=fitbit+charge+4%2Caps%2C147&sr=8-3'
    products = [(url, 100)]

    products_below_price = []
    for product_url, limit in products:
        title, price, available = get_product_info(product_url)
        if title is not None and price <= limit and available:
            products_below_price.append((url, title, price))
    if products_below_price:
        message = 'Subject: New products!\n\n'
        message += 'Found {} new products!\n\n'.format(
            len(products_below_price))
        for url, title, price in products_below_price:
            message += f"{title}\n\n"
            message += f"Price: {price}\n\n"
            message += f"{url}\n\n"
        send_email(message, 'jamesmichaelstacy@gmail.com')
