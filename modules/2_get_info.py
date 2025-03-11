import load_django
import requests
from bs4 import BeautifulSoup
import re
from parser_app.models import PropertyInfo


def scrape_property(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    try:
        images = [img['src'] for img in soup.find_all('img', class_='mbSlideDown') if 'src' in img.attrs]
    except Exception:
        images = []

    try:
        name = soup.find('h1', class_='font_sarabun show-title').text.strip()
    except AttributeError:
        name = 'N/A'

    try:
        cost = soup.find('div', class_='t-24 price-detail mt-0 price_topic').find('b').text.strip()
    except AttributeError:
        cost = 'N/A'

    property_dict = {}
    try:
        spans = soup.find('div', class_="row detail-row")
        spansText = spans.find_all('span', class_='detail-property-list-text')
        spansTitle = spans.find_all('span', class_='detail-property-list-title')
        for title, text in zip(spansTitle, spansText):
            property_dict[title.get_text().strip()] = text.get_text().strip()
    except AttributeError:
        pass

    try:
        wordwrap = soup.find('p', class_='wordwrap').text.strip()
    except AttributeError:
        wordwrap = 'N/A'

    highlights = []
    try:
        highlights = [span.get_text().strip() for span in soup.find_all('span', class_='text_property_highlight')]
    except AttributeError:
        pass

    try:
        address = soup.find('div', class_='detail-text-zone').text.strip()
    except AttributeError:
        address = 'N/A'

    try:
        location = soup.find('div', class_='detail-text-project').text.strip()
    except AttributeError:
        location = 'N/A'

    try:
        more_about_place = soup.find('div', class_='box-show-text-all-project').text.strip()
    except AttributeError:
        more_about_place = 'N/A'

    places = []
    try:
        nearPlaces = soup.find('div', class_='detail-nearbyList elems-nearby')
        places = [nearPlace.get_text().strip() for nearPlace in nearPlaces.find_all('a', class_='box-name-manu-map')]
    except AttributeError:
        pass

    seller_info = {}
    try:
        seller_info = {
            'name': soup.find(id='nameOwner').find('label').text.strip(),
            'Verified': soup.find('span', class_='id-verify-text mr-1').text.strip(),
            'Stars': soup.find('p', class_='rwCTAclick text_review').text.strip(),
            'Id': re.search(r"gotoReviewpage\('(\d+)'\)",
                            soup.find('p', class_='rwCTAclick', onclick=True)['onclick']).group(1)
        }
    except (AttributeError, TypeError):
        seller_info = {'name': 'N/A', 'Verified': 'N/A', 'Stars': 'N/A', 'Id': 'N/A'}

    try:
        whatsapp = soup.find('a', class_='OwnerProfileContact-active co-whatsapp')['href']
    except (AttributeError, TypeError):
        whatsapp = 'N/A'


    PropertyInfo.objects.update_or_create(
        url=url,
        defaults={
            'images': ','.join(images),
            'name': name,
            'cost': cost,
            'details': str(property_dict),
            'wordwrap': wordwrap,
            'highlights': ','.join(highlights),
            'address': address,
            'location': location,
            'about_place': more_about_place,
            'nearby_places': ','.join(places),
            'seller_info': seller_info,
            'whatsapp': whatsapp,
        }
    )


def scrape_all_properties():
    from parser_app.models import Listing
    urls = Listing.objects.values_list('url', flat=True)
    for url in urls:
        scrape_property(url)
        print(f'Scraped: {url}')


scrape_all_properties()
