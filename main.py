import pandas as pd
import requests
from bs4 import BeautifulSoup

# Homepage
base_url = 'https://www.sellyourmac.com'
products = []
urls = []


def data(product=None, url=None):
    if product is None:
        urls.append(url)
    else:
        products.append(product)


def frame():
    return {
        'Products': products,
        'Urls': urls
    }


def scrape_base_url(url):
    web_page = requests.get(url)
    if web_page.status_code != 200:
        print(f"Error: {web_page.status_code}")
        return None
    return BeautifulSoup(web_page.content, 'html.parser')


def scrape_products(web_page):
    if web_page is None:
        return
    products = web_page.find_all('li', class_="uk-margin-small-bottom")
    for product in products:
        scrape_product_names(product)
        scrape_product_urls(product)


def scrape_product_names(product):
    product = product.find('span', class_="uk-text-medium")
    if product:
        data(product.text.strip(), None)


def scrape_product_urls(product):
    url = product.find('a', class_="level_button")
    if url:
        data(None, base_url + url['href'])


if __name__ == "__main__":
    web_page = scrape_base_url(base_url)
    scrape_products(web_page)
    df = pd.DataFrame(frame())
    df.to_csv('test.csv', index=None)
