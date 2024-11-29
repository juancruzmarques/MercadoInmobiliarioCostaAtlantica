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
            pubs = soup.find_all(class_='CardContainer-sc-1tt2vbg-5 fvuHxG')

            for pub in pubs:
                price = pub.find(class_='postingPrices-module__price__fqpP5').text
                posting_address = pub.find('div', class_='postingLocations-module__location-address__k8Ip7 postingLocations-module__location-address-in-listing__UQS03')
                location = pub.find(class_='postingLocations-module__location-text__Y9QrY').text

                if posting_address == None: 
                    posting_address = 'N/A'
                else: 
                    posting_address = posting_address.text

                main_features = pub.find('h3', class_='postingMainFeatures-module__posting-main-features-block__se1F_ postingMainFeatures-module__posting-main-features-block-one-line__BFUdC')

                if main_features == None:
                    continue
                else:
                    main_features = main_features.find_all('span')
                    features = dict()
                    for feature in main_features:
                        feature_split = feature.text.split(' ')
                        features[feature_split[1]] = feature_split[0]
                publication = dict()
                publication['price'] = price
                publication['posting_address'] = posting_address 
                publication['location'] = location
                publication.update(features)
                print(publication)




            print(f'PAGINA {page} FINALIZADA')
