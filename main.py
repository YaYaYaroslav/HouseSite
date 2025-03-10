import requests
from bs4 import BeautifulSoup
import re

url = 'https://www.livinginsider.com/livingdetail/2541819/⭐-ขายคอนโดใกล้-bts-นานา-⭐-สุขุมวิท-สวีท-2-ห้องนอน-2-ห้องน้ำ-78-ตรม-จอดรถได้-2-คัน.html'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

response = requests.get(url, headers=headers)

soup = BeautifulSoup(response.content, 'html.parser')

images = soup.find_all('img', class_='mbSlideDown')
image_links = [img['src'] for img in images if 'src' in img.attrs]
print(f'images: {image_links}')

TextUnderImages = soup.find('h1', class_='font_sarabun show-title').text.strip()
print(f'name: {TextUnderImages}')

cost = soup.find('div', class_='t-24 price-detail mt-0 price_topic').find('b').text.strip()
print(f'cost: {cost}')

spans = soup.find('div', class_="row detail-row")

spansText = spans.find_all('span', class_='detail-property-list-text')
spansTitle = spans.find_all('span', class_='detail-property-list-title')

property_dict = {}
for title, text in zip(spansTitle, spansText):
    partTitle = title.get_text().strip().replace(" ", "")
    partText = text.get_text().strip().replace(" ", "")
    property_dict[partTitle] = partText

print(property_dict)


wordwrap = soup.find('p', class_='wordwrap').text.strip()
print(wordwrap)

propertyHighlights = soup.find('div', class_="box_property_highlight")
propertyHighlightLists = propertyHighlights.find_all('span', class_='text_property_highlight')

HighlightLists = []

for propertyHighlightList in propertyHighlightLists:
    partText = propertyHighlightList.get_text().strip()
    HighlightLists.append(partText)

print(HighlightLists)

address = soup.find('div', class_='detail-text-zone').text.strip()
print(address)
location = soup.find('div', class_='detail-text-project').text.strip()
print(location)
moreAboutPlace = soup.find('div', class_='box-show-text-all-project').text.strip()
print(moreAboutPlace)

nearPlaces = soup.find('div', class_='detail-nearbyList elems-nearby')
places = [nearPlace.get_text().strip() for nearPlace in nearPlaces.find_all('a', class_='box-name-manu-map')]

print(places)

inAreas = soup.find('ul', class_='mt-1')
inArea = inAreas.find_all('li', class_='box-link-map box-link-google-map active-open')

inAreas_dict = {}
for area in inArea:
    partTitle = area.get_text().strip()
    partText = area.find('p').get_text() if area.find('p') else None
    inAreas_dict[partTitle] = partText

print(inAreas_dict)

sellerInfo = {}

sellerInfo['name'] = soup.find(id='nameOwner').find('label').text.strip()
sellerInfo['Verified'] = soup.find('span', class_='id-verify-text mr-1').text.strip()
sellerInfo['Stars'] = soup.find('p', class_='rwCTAclick text_review').text.strip()
sellerInfo['Id'] = re.search(r"gotoReviewpage\('(\d+)'\)", soup.find('p', class_='rwCTAclick', onclick=True)['onclick']).group(1)

print(sellerInfo)


whatsapp = soup.find('a', class_='OwnerProfileContact-active co-whatsapp')['href']
print(whatsapp)

nowOnThisAd = soup.find('div', class_='alert alert-dismissible').find('strong').text

print(nowOnThisAd)