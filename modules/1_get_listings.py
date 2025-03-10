import load_django

import requests
from bs4 import BeautifulSoup
from parser_app.models import Listing

BASE_URL = ["https://www.livinginsider.com/living_zone/21/all/all/", "/พระราม8-สามเสน.html"]
PAGES_TO_SCRAPE = 5


def get_listings(page):
    url = f"{BASE_URL[0]}{page}{BASE_URL[1]}"
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Помилка запиту {url}")
        return []

    soup = BeautifulSoup(response.content, "html.parser")
    listings = []

    for item in soup.find_all("div", class_="col-md-3 col-sm-4 col-xs-6 padding_topic margin_top_topic"):
        title_tag = item.find("p", class_="font-Sarabun margin-0")
        link_tag = item.find("a", href=True)

        if title_tag and link_tag:
            title = title_tag.text.strip()
            url = link_tag["href"]
            listings.append((title, url))

    print(listings)
    return listings


def save_to_db(listings):
    for title, url in listings:
        Listing.objects.get_or_create(title=title, url=url)


if __name__ == "__main__":
    all_listings = []

    for page in range(1, PAGES_TO_SCRAPE + 1):
        listings = get_listings(page)
        all_listings.extend(listings)
        print(f"Зібрано {len(listings)} записів зі сторінки {page}")

    save_to_db(all_listings)
    print("Дані збережено у БД Django.")