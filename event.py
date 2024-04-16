import requests
from bs4 import BeautifulSoup

url = 'https://www.eventernote.com/actors/水瀬いのり/2890/events?actor_id=2618&limit=800&page=1'

response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

events = soup.find_all('li', class_='clearfix')

with open('events_inori.txt', 'w', encoding='utf-8') as file:
    file.write('Date,Title,Venue\n')  # ヘッダー行を書き込む
    for event in events:
        date_elem = event.find('p', class_=lambda value: value and 'day' in value)
        date = date_elem.text.strip() if date_elem else 'Date not available'

        title_elem = event.find('h4')
        title = title_elem.text.strip() if title_elem else 'Title not available'

        venue_elem = event.find('div', class_='place')
        venue = venue_elem.text.strip() if venue_elem else 'Venue not available'

        file.write(f'{date},{title},{venue}\n')

