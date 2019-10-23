from bs4 import BeautifulSoup
import pandas as pd
import requests


cards = []

url = 'https://alura-site-scraping.herokuapp.com/index.php'
req = requests.get(url)
soup = BeautifulSoup(req.text, 'html.parser')
pages = int(soup.find('span', class_="info-pages").get_text().split()[-1])

for i in range(pages):

    url = f'https://alura-site-scraping.herokuapp.com/index.php?page={(i + 1)}'
    req = requests.get(url)
    soup = BeautifulSoup(req.text, 'html.parser')

    anuncios = soup.find('div', {"id": "container-cards"}).findAll('div', class_="card")

    for anuncio in anuncios:
        card = {}

        card['value'] = anuncio.find('p', {'class': 'txt-value'}).getText()

        infos = anuncio.find('div', {'class': 'body-card'}).findAll('p')
        for info in infos:
            card[info.get('class')[0].split('-')[-1]] = info.get_text()

        items = anuncio.find('div', {'class': 'body-card'}).ul.findAll('li')
        items.pop()
        acessorios = []
        for item in items:
            acessorios.append(item.get_text().replace('► ', ''))
        card['items'] = acessorios

        cards.append(card)
    

dataset = pd.DataFrame(cards)