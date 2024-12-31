from tools.proxy_tool import ProxyList
from bs4 import BeautifulSoup
import re
import math 
import cloudscraper
import datetime
import time
import sqlite3
import concurrent.futures
import mysql.connector

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

    

# 'Workers' sería la cantidad de instancias que quiero.
# Segun la cantidad de instacias, los rangos de páginas.
# Si quiero que las instancias se definan dentro de la clase necesito otro metodo que sea el generador de los workers. 
# Es decir, que la implementación del multi process se hace dentro de la clase. 
# Pero a la hora scrapear se decide si se hace simple o multi proceso (Que eventualmente será el pordefecto).
    def get_pubs(self, rangoss: list):
        # Quiero que se cree una base de datos para cada rango de páginas, es decir para cada processo o worker
        page_range = rangoss



        local_scraper = cloudscraper.create_scraper(browser={
        'browser': 'firefox',
        'platform': 'linux',
        'desktop': True
    })

        conn = 0
        cur = 0
        conn = mysql.connector.connect(host="127.0.0.1", port=3306, user="Juancito", password="new_password", database="ZonaProp_db", charset="utf8mb4", collation="utf8mb4_general_ci")
        cur = conn.cursor()

        for page in page_range:
            if page == 1:
                modified_url = self.base_url + '-orden-precio-descendente' + ".html"
            else:
                modified_url = self.base_url + '-orden-precio-descendente'+ '-pagina-'+ str(page)+ ".html"
            print(f'Accesed url:  {modified_url}')


            try:
                response = local_scraper.get(modified_url, proxies=self.proxy_pool.get_proxy()).text
            except:
                # Si hay algún tipo de error con la proxy utilizada salta a la siguiente
                response = local_scraper.get(modified_url, proxies=self.proxy_pool.get_proxy()).text

            soup = BeautifulSoup(response, "html.parser")   
            pubs = soup.find_all(class_='CardContainer-sc-1tt2vbg-5 fvuHxG')

            batch = []
            repeated = []
            for pub in pubs:
                publication = dict()
                publication['posting_address'] = None
                publication['price'] = None
                publication['location'] = None



                price = float(pub.find(class_='postingPrices-module__price__fqpP5').text.split(' ')[1].replace('.', ''))
                posting_address = pub.find('div', class_='postingLocations-module__location-address__k8Ip7 postingLocations-module__location-address-in-listing__UQS03')
                location = pub.find(class_='postingLocations-module__location-text__Y9QrY').text

                pictures = pub.find('span', class_='postingMultimediaTags-module__tag-info__oapbv')
                if pictures == None:
                    pictures = None
                else:
                    pictures = int(pictures.text)

                if posting_address == None: 
                    posting_address = None
                else: 
                    posting_address = posting_address.text

                expenses = pub.find('div', class_='postingPrices-module__expenses__Ow5oa postingPrices-module__expenses-property-listing__Fhn8x')
                if expenses == '' or expenses == None:
                    expenses = None
                    expenses_currency = None
                else:
                    expenses_parts = expenses.text.split(' ')
                    if len(expenses_parts) == 1:
                        expenses = None
                        expenses_currency = None
                    else:
                        expenses = float(expenses_parts[1].replace('.', ''))
                        expenses_currency = expenses_parts[0]

                description = pub.find('h3', class_='postingCard-module__posting-description__r17OH')
                if description == None:
                    description = None
                else:
                    description = description.text

                main_features = pub.find('h3', class_='postingMainFeatures-module__posting-main-features-block__se1F_ postingMainFeatures-module__posting-main-features-block-one-line__BFUdC')
                link = pub.find('h3', class_='postingCard-module__posting-description__r17OH')
                    
                if link == None:
                    link = None
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
                publication['m²'] = None
                publication['amb.'] = None
                publication['dorm.'] = None
                publication['baños'] = None
                publication['coch.'] = None
                if main_features == None:
                    continue
                else:
                    main_features = main_features.find_all('span')
                    for feature in main_features:
                        feature_split = feature.text.split(' ')
                        if feature_split[1] == 'm²':
                            publication['m²'] = int(feature_split[0])
                        if feature_split[1] == 'amb.':
                            publication['amb.'] = int(feature_split[0])
                        if feature_split[1] == 'dorm.':
                            publication['dorm.'] = int(feature_split[0])
                        if feature_split[1] == 'baños':
                            publication['baños'] = int(feature_split[0])
                        if feature_split[1] == 'coch.':
                            publication['coch.'] = int(feature_split[0])
                publication['link'] = link
                publication['identification'] = identification
                publication['last_update'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                if description is not None:
                    publication['description'] = description[:49]
                else:
                    publication['description'] = None


                valores = (publication['price'], publication['expenses_currency'], publication['expenses'], publication['posting_address'], publication['pictures'], publication['location'], publication['m²'], publication['amb.'], publication['dorm.'], publication['baños'], publication['coch.'],publication['link'],publication['identification'], publication['last_update'], publication['description'])
                batch.append(valores)
                print(publication['price'])


                query = '''INSERT INTO Propiedades(precio, moneda_expensas, expensas, nombre, fotos, localizacion, metros_cuadrados, ambientes, dormitorios, baños, cocheras, link, id_zonaprop, ultima_actualizacion, descripcion) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'''


                try:
                    cur.execute(query, valores)
                except:
                    repeated.append(publication['id_zonaprop'])
                    print(f'################### ERROR!      {repeated} ###################')

            conn.commit()
            print(f'PAGINA {page}/{rangoss[-1]} DE {self.pages} FINALIZADA')

    def get_pubs_multi(self, number_of_workers):
        numero_de_paginas = self.get_pages()
        intervalo = math.ceil(numero_de_paginas / number_of_workers)

        rango = list()
        count = 0
        ultimo_rango = 1
        for i in range(1, number_of_workers + 1):
            count +=1
            if intervalo * i > numero_de_paginas:
                rango.append(range(ultimo_rango, numero_de_paginas + 1))
            else:
                rango.append(range(ultimo_rango, intervalo * i + 1))
                # Estos rangos son lo que le corresponde a cada worker.
            ultimo_rango = ultimo_rango + intervalo

        with concurrent.futures.ProcessPoolExecutor() as executor:
            executor.map(self.get_pubs, rango)
