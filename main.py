import requests
from bs4 import BeautifulSoup
import re

url = 'https://www.livinginsider.com/livingdetail/2541819/⭐-ขายคอนโดใกล้-bts-นานา-⭐-สุขุมวิท-สวีท-2-ห้องนอน-2-ห้องน้ำ-78-ตรม-จอดรถได้-2-คัน.html'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.content, 'html.parser')


try:
    images = soup.find_all('img', class_='mbSlideDown')
    image_links = [img['src'] for img in images if 'src' in img.attrs]
except Exception:
    image_links = []

try:
    TextUnderImages = soup.find('h1', class_='font_sarabun show-title').text.strip()
except AttributeError:
    TextUnderImages = 'N/A'

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
        partTitle = title.get_text().strip().replace(" ", "")
        partText = text.get_text().strip().replace(" ", "")
        property_dict[partTitle] = partText
except AttributeError:
    pass

try:
    wordwrap = soup.find('p', class_='wordwrap').text.strip()
except AttributeError:
    wordwrap = 'N/A'

HighlightLists = []
try:
    propertyHighlights = soup.find('div', class_="box_property_highlight")
    propertyHighlightLists = propertyHighlights.find_all('span', class_='text_property_highlight')
    for propertyHighlightList in propertyHighlightLists:
        partText = propertyHighlightList.get_text().strip()
        HighlightLists.append(partText)
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
    moreAboutPlace = soup.find('div', class_='box-show-text-all-project').text.strip()
except AttributeError:
    moreAboutPlace = 'N/A'

places = []
try:
    nearPlaces = soup.find('div', class_='detail-nearbyList elems-nearby')
    places = [nearPlace.get_text().strip() for nearPlace in nearPlaces.find_all('a', class_='box-name-manu-map')]
except AttributeError:
    pass

inAreas_dict = {}
try:
    inAreas = soup.find('ul', class_='mt-1')
    inArea = inAreas.find_all('li', class_='box-link-map box-link-google-map active-open')
    for area in inArea:
        partTitle = area.get_text().strip()
        partText = area.find('p').get_text() if area.find('p') else None
        inAreas_dict[partTitle] = partText
except AttributeError:
    pass

sellerInfo = {}
try:
    sellerInfo['name'] = soup.find(id='nameOwner').find('label').text.strip()
    sellerInfo['Verified'] = soup.find('span', class_='id-verify-text mr-1').text.strip()
    sellerInfo['Stars'] = soup.find('p', class_='rwCTAclick text_review').text.strip()
    sellerInfo['Id'] = re.search(r"gotoReviewpage\('(\d+)'\)", soup.find('p', class_='rwCTAclick', onclick=True)['onclick']).group(1)
except (AttributeError, TypeError):
    sellerInfo = {'name': 'N/A', 'Verified': 'N/A', 'Stars': 'N/A', 'Id': 'N/A'}

try:
    whatsapp = soup.find('a', class_='OwnerProfileContact-active co-whatsapp')['href']
except (AttributeError, TypeError):
    whatsapp = 'N/A'

try:
    nowOnThisAd = soup.find('div', class_='alert alert-dismissible').find('strong').text
except AttributeError:
    nowOnThisAd = 'N/A'


print(f'images: {image_links}')
print(f'name: {TextUnderImages}')
print(f'cost: {cost}')
print(property_dict)
print(wordwrap)
print(HighlightLists)
print(address)
print(location)
print(moreAboutPlace)
print(places)
print(inAreas_dict)
print(sellerInfo)
print(whatsapp)
print(nowOnThisAd)