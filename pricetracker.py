#!/usr/bin/env python3

from math import prod
import requests
from bs4 import BeautifulSoup
import unicodedata
import json

from send_email import send_email

AVAIL_VAL = '.a-color-success'

HEADERS = ({'User-Agent':
            'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',
            'Accept-Language': 'en-US, en;q=0.5'})

SAVE_DATA = 'products.json'


def load_product(filepath):
    try:
        with open(filepath, 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        data = []
    return data


def get_product_info(url):
    page = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(page.content, features="lxml")

    try:
        title = soup.find(id='productTitle').get_text().strip()
        price_str = soup.find(class_='a-price-whole').get_text()
        # print(title, price_str)
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

    # print(title, price, available)
    return title, price, available


if __name__ == '__main__':
    products = load_product(SAVE_DATA)
    # print(products)

    products_below_price = []
    products_above_price = []
    for dict in products:
        # print(dict['url'])
        url = dict['url']
        limit = dict['limit']
        title, price, available = get_product_info(url)
        # print(title, price, available)
        if title is not None and price <= limit and available:
            # print("Below", title, price, available)
            products_below_price.append((url, title, price, limit))
        elif title is not None and price > limit and available:
            # print("Above", title, price, available)
            products_above_price.append((url, title, price, limit))
    if products_below_price or products_above_price:
        print("Ready to send email")
        message = 'Subject: Tracked products!\n\n'
        if products_below_price:
            message += 'Found {} products below your target price!\n\n'.format(
                len(products_below_price))
            for url, title, price, limit in products_below_price:
                message += f"{title}\n"
                message += f"\t- Price: $ {price}\t\t| Limit: $ {limit}\n"
                message += f"\t- {url}\n\n"
        if products_above_price:
            message += 'Found {} products above your target price!\n\n'.format(
                len(products_above_price))
            for url, title, price, limit in products_above_price:
                message += f"{title}\n"
                message += f"\t- Price: $ {price}\t\t| Limit: $ {limit}\n"
                message += f"\t- {url}\n\n"
        # print(message)
        send_email(message, 'jamesmichaelstacy@gmail.com')
    else:
        print('No products found')
