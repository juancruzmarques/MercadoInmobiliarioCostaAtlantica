from tools.proxy_tool import ProxyList
from bs4 import BeautifulSoup
import re
import math 
import cloudscraper

class Scraper:
    def __init__(self, base_url: str, proxy: ProxyList)-> None:    
        self.proxy_pool: ProxyList= proxy
        self.base_url = base_url.replace('.html', '')
        self.scraper = cloudscraper.create_scraper(browser={
        'browser': 'firefox',
        'platform': 'linux',
        'desktop': True
    })
        self.pages = None

    def get_pages (self):
    # Encuentr el numero de paginas
        response = self.scraper.get(self.base_url + ".html", proxies=self.proxy_pool.get_proxy()).text
        soup = BeautifulSoup(response, "html.parser")   
        cantidad_prop = soup.find(class_="Title-sc-1oqs0ed-0 kNcbvY")
    # Evita errores de "tipos" para strings
        if cantidad_prop is not None:
            cantidad_prop = cantidad_prop.text
        else:
             cantidad_prop = ""
        paginas = re.search(r'^\d+(?:\.\d+)?', str(cantidad_prop))
    # Evita errores de "tipos" para integers
        if paginas is not None:
            paginas = int(paginas.group().replace('.', ''))
        else:
            paginas = 1
        paginas = math.ceil(paginas/30)
        self.pages = paginas
        return paginas
    
    def get_pubs(self):
        for page in range(1, self.get_pages()):
            if page == 1:
                modified_url = self.base_url + '-orden-precio-descendente' + ".html"
            else:
                modified_url = self.base_url + '-orden-precio-descendente'+ '-pagina-'+ str(page)+ ".html"
            print(f'Accesed url:     {modified_url}')
            response = self.scraper.get(modified_url, proxies=self.proxy_pool.get_proxy()).text
            soup = BeautifulSoup(response, "html.parser")   
            pubs = soup.find_all(class_='PostingContainer-sc-i1odl-2 iQlPeD')
            for pub in pubs:
                price = pub.find(class_='Price-sc-12dh9kl-3 geYYII').text
                location = pub.find('div', class_='LocationAddress-sc-ge2uzh-0 iylBOA postingAddress')
                

                if location == None: 
                    location = 'N/A'
                else: 
                    location = location.text
                main_features = pub.find('h3', class_='PostingMainFeaturesBlock-sc-1uhtbxc-0 cHDgeO')

                if main_features == None:
                    continue
                else:
                    y = [sqm, room, bedroom, baths, parking]
                    for y, x in len(main_features.find_all('span'))+1:
                    y = main_features.find_all('span')[x]
                    if y == None:
                        y = 'N/A'
                    else: y = y.text
                print(f'|   {price}   |   {location}   |   {sqm}   |')

            print(f'PAGINA {page} FINALIZADA')
