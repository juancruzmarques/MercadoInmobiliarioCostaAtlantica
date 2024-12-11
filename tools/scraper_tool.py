from tools.proxy_tool import ProxyList
from bs4 import BeautifulSoup
import re
import math 
import cloudscraper
import time
import sqlite3

class Scraper:
    def __init__(self, base_url: str, proxy: ProxyList)-> None:    
        self.proxy_pool: ProxyList= proxy
        self.base_url = base_url.replace('.html', '')
        self.scraper = cloudscraper.create_scraper(browser={
        'browser': 'firefox',
        'platform': 'linux',
        'desktop': True
    })
        self.pubs = None
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
        conn = sqlite3.connect('ZonaPropData')
        cur = conn.cursor()

        cur.execute('''
                        CREATE TABLE IF NOT EXISTS Propiedades(
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            precio FLOAT,
                            moneda_expensas TEXT,
                            expensas FLOAT,
                            nombre TEXT,
                            fotos INT,
                            localizacion TEXT,
                            metros_cuadrados INT,
                            ambientes INT,
                            dormitorios INT,
                            baños INT,
                            cocheras INT,
                            link TEXT,
                            id_zonaprop INT,
                            ultima_actualizacion TIMESTAMP,
                            descripcion TEXT
                        )
                    ''')

        for page in range(1, self.get_pages()+1):
            if page == 1:
                modified_url = self.base_url + '-orden-precio-descendente' + ".html"
            else:
                modified_url = self.base_url + '-orden-precio-descendente'+ '-pagina-'+ str(page)+ ".html"
            print(f'Accesed url:  {modified_url}')

            try:
                response = self.scraper.get(modified_url, proxies=self.proxy_pool.get_proxy()).text
            except:
                # Si hay algún tipo de error con la proxy utilizada salta a la siguiente
                response = self.scraper.get(modified_url, proxies=self.proxy_pool.get_proxy()).text

            soup = BeautifulSoup(response, "html.parser")   
            pubs = soup.find_all(class_='CardContainer-sc-1tt2vbg-5 fvuHxG')

            for pub in pubs:
                publication = dict()
                price = float(pub.find(class_='postingPrices-module__price__fqpP5').text.split(' ')[1].replace('.', ''))
                posting_address = pub.find('div', class_='postingLocations-module__location-address__k8Ip7 postingLocations-module__location-address-in-listing__UQS03')
                location = pub.find(class_='postingLocations-module__location-text__Y9QrY').text

                pictures = pub.find('span', class_='postingMultimediaTags-module__tag-info__oapbv')
                if pictures == None:
                    pictures = 'N/A'
                else:
                    pictures = int(pictures.text)

                if posting_address == None: 
                    posting_address = 'N/A'
                else: 
                    posting_address = posting_address.text

                expenses = pub.find('div', class_='postingPrices-module__expenses__Ow5oa postingPrices-module__expenses-property-listing__Fhn8x')
                if expenses == '' or expenses == None:
                    expenses = 'N/A'
                    expenses_currency = 'N/A'
                else:
                    expenses_parts = expenses.text.split(' ')
                    if len(expenses_parts) == 1:
                        expenses = 'N/A'
                        expenses_currency = 'N/A'
                    else:
                        expenses = float(expenses_parts[1].replace('.', ''))
                        expenses_currency = expenses_parts[0]

                description = pub.find('h3', class_='postingCard-module__posting-description__r17OH')
                if description == None:
                    description = 'N/A'
                else:
                    description = description.text

                main_features = pub.find('h3', class_='postingMainFeatures-module__posting-main-features-block__se1F_ postingMainFeatures-module__posting-main-features-block-one-line__BFUdC')
                link = pub.find('h3', class_='postingCard-module__posting-description__r17OH')
                    
                if link == None:
                    link = 'N/A'
                    identification = 0
                else:
                    link = 'https://www.zonaprop.com.ar' + link.find('a').get('href')
                    identification = int(link.split('-')[-1].replace('.html', ''))

                publication['price'] = price
                publication['expenses_currency'] = expenses_currency
                publication['expenses'] = expenses
                publication['posting_address'] = posting_address 
                publication['pictures'] = pictures
                publication['location'] = location
                publication['m²'] = 'N/A'
                publication['amb.'] = 'N/A'
                publication['dorm.'] = 'N/A'
                publication['baños'] = 'N/A'
                publication['coch.'] = 'N/A'
                if main_features == None:
                    continue
                else:
                    main_features = main_features.find_all('span')
                    for feature in main_features:
                        feature_split = feature.text.split(' ')
                        if feature_split[1] == 'm²':
                            publication['m²'] = feature_split[0]
                        if feature_split[1] == 'amb.':
                            publication['amb.'] = feature_split[0]
                        if feature_split[1] == 'dorm.':
                            publication['dorm.'] = feature_split[0]
                        if feature_split[1] == 'baños':
                            publication['baños'] = feature_split[0]
                        if feature_split[1] == 'coch.':
                            publication['coch.'] = feature_split[0]
                publication['link'] = link
                publication['identification'] = identification
                publication['last_update'] = time.strftime("%d/%m/%Y %H:%M:%S")
                publication['description'] = description


                #print(publication)

                cur.execute(
                        '''
                            INSERT INTO Propiedades(
                                precio, moneda_expensas, expensas, nombre, fotos, localizacion, metros_cuadrados, ambientes, dormitorios, baños, cocheras, link, id_zonaprop, ultima_actualizacion, descripcion
                            ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
                        ''', (publication['price'], publication['expenses_currency'], publication['expenses'], publication['posting_address'], publication['pictures'], publication['location'], publication['m²'], publication['amb.'], publication['dorm.'], publication['baños'], publication['coch.'],publication['link'],publication['identification'], publication['last_update'], publication['description'])
                        )
            conn.commit()
            print(f'PAGINA {page} DE {self.pages} FINALIZADA')
