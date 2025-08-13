from tools.proxy_tool import ProxyList
import base64
from bs4 import BeautifulSoup
import re
import math 
import cloudscraper
import datetime
import concurrent.futures
import mysql.connector
from mysql.connector import Error
import json

class Scraper:
    def __init__(self, base_url: str, proxy: ProxyList, db_table_name)-> None:    
        """
        Constructor de la herramienta para escrapear.
        """
        self.proxy_pool: ProxyList= proxy
        self.base_url = base_url.replace('.html', '')
        self.scraper = cloudscraper.create_scraper(browser={
        'browser': 'firefox',
        'platform': 'linux',
        'desktop': True
    })
        self.pubs = None
        self.pages = None
        self.dbtable = db_table_name
        
    def get_pages (self):
        '''
        Obtiene el numero de páginas para dicha consulta a zonaprop.
        '''
    # Encuentr el numero de paginas
        response = self.scraper.get(self.base_url + ".html", proxies=self.proxy_pool.get_proxy()).text
        soup = BeautifulSoup(response, "html.parser")   
        cantidad_prop = soup.find(class_="postingsTitle-module__title") #Title-sc-1oqs0ed-0 kNcbvY

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
        """
        Obtiene las publicaciónes dentro de un rango de páginas definido.
        """
        # Quiero que se cree una base de datos para cada rango de páginas, es decir para cada processo o worker
        page_range = rangoss

        local_scraper = cloudscraper.create_scraper(browser={
        'browser': 'chrome',
        'platform': 'linux',
        'desktop': True
    })

        # Acá está el problema 29-05-25
        try:
            conn = mysql.connector.connect(host="127.0.0.1", port=3306, user="Juancito", password="0223", database="ZonaProp_db", charset="utf8mb4", collation="utf8mb4_general_ci")
            cur = conn.cursor()
        except Error as e:
            print(f'Error! : {e}')
            raise RuntimeError(f'Error! : {e}')
            

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
            pubs = soup.find_all(class_='postingCard-module__posting-container')

            batch = []
            for pub in pubs:
                publication = dict()
                publication['posting_address'] = None
                publication['price'] = None
                publication['location'] = None



                price = float(pub.find(class_='postingPrices-module__price').text.split(' ')[1].replace('.', '')) #postingPrices-module__price__fqpP5
                posting_address = pub.find('div', class_='postingLocations-module__location-address postingLocations-module__location-address-in-listing') #postingLocations-module__location-address__k8Ip7 postingLocations-module__location-address-in-listing__UQS03
                location = pub.find(class_='postingLocations-module__location-text').text #postingLocations-module__location-text__Y9QrY

                pictures = pub.find('span', class_='postingMultimediaTags-module__tag-info') #postingMultimediaTags-module__tag-info__oapbv
                if pictures == None:
                    pictures = None
                else:
                    pictures = int(pictures.text)

                if posting_address == None: 
                    posting_address = None
                else: 
                    posting_address = posting_address.text

                expenses = pub.find('div', class_='postingPrices-module__expenses postingPrices-module__expenses-property-listing') #postingPrices-module__expenses__Ow5oa postingPrices-module__expenses-property-listing__Fhn8x
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

                description = pub.find('h3', class_='postingCard-module__posting-description') #postingCard-module__posting-description__r17OH
                if description == None:
                    description = None
                else:
                    description = description.text

                main_features = pub.find('h3', class_='postingMainFeatures-module__posting-main-features-block postingMainFeatures-module__posting-main-features-block-one-line') #postingMainFeatures-module__posting-main-features-block__se1F_ postingMainFeatures-module__posting-main-features-block-one-line__BFUdC
                link = pub.find('h3', class_='postingCard-module__posting-description') #postingCard-module__posting-description__r17OH
                    
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


                print(publication)
                valores = (publication['price'], publication['expenses_currency'], publication['expenses'], publication['posting_address'], publication['pictures'], publication['location'], publication['m²'], publication['amb.'], publication['dorm.'], publication['baños'], publication['coch.'],publication['link'],publication['identification'], publication['last_update'], publication['description'])
                batch.append(valores)

                cur.execute(f'''SELECT * FROM {self.dbtable} WHERE link = %s''', (publication['link'],) )

                looking_for_dup = len(cur.fetchall())

                if looking_for_dup == 0 or None:
                    query = f'''INSERT INTO {self.dbtable} (precio, moneda_expensas, expensas, nombre, fotos, localizacion, metros_cuadrados, ambientes, dormitorios, baños, cocheras, link, id_zonaprop, ultima_actualizacion, descripcion) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'''

                    print(f"Guardando:  {publication['posting_address']}")
                    cur.execute(query, valores)
                else:
                    cant_rep = looking_for_dup
                    print(f'REPETIDO {cant_rep}')

            conn.commit()
            print(f'PAGINA {page}/{rangoss[-1]} DE {self.pages} FINALIZADA')

    def get_pubs_multi(self, number_of_workers=1):
        """
        Obtiene las publicaciones de forma concurrente o en paralelo definido por el numero de instacias 'number of workers' indicado en la función. Por default es 1.
        """
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

    def expand_data(self, rango: list):
        limite_inferior = rango[0]
        limite_superior = rango[-1]
        print(limite_inferior, limite_superior)

        local_scraper = cloudscraper.create_scraper(browser={
        'browser': 'chrome',
        'platform': 'linux',
        'desktop': True
        })

        conn = mysql.connector.connect(host="127.0.0.1", port=3306, user="Juancito", password="0223", database="ZonaProp_db", charset="utf8mb4", collation="utf8mb4_general_ci")
        cur = conn.cursor() 

        cur.execute(
                f'''
                SELECT
                    id,
                    link
                FROM
                    {self.dbtable}
                WHERE
                    id > {limite_inferior}
                AND
                    id < {limite_superior}
                '''
                )

        pubs: list
        pubs = cur.fetchall() 

        for pub in pubs:
            pub_id = pub[0]
            pub_link = pub[1]

            response = local_scraper.get(pub_link, proxies=self.proxy_pool.get_proxy())
            print(f'Link visitado:    {pub_link}')
            print(response.status_code)
            if response.status_code != 200:
                continue

            soup = BeautifulSoup(response.text, "html.parser")

            script_tags = soup.find_all('script', string=True)

            for script in script_tags:
                publication_data = {}

                # Extract Base64 strings using regex
                lat_match = re.search(r'mapLatOf\s*=\s*"([^"]+)"', script.string)
                lng_match = re.search(r'mapLngOf\s*=\s*"([^"]+)"', script.string)


                if lat_match and lng_match:
                    # Decode the Base64 strings
                    latitude = base64.b64decode(lat_match.group(1)).decode('utf-8')
                    longitude = base64.b64decode(lng_match.group(1)).decode('utf-8')
                    publication_data["latitude"] = latitude
                    publication_data["longitude"] = longitude 
                else:
                    publication_data["latitude"] = None
                    publication_data["longitude"] = None


# De acá solo me interesa el tipo de propiedad que me va a facilitar clasificarlas cuando tenga a todos los tipos
                data_layer_info = re.search(r'dataLayerInfo\s*=\s*\{(.*?)\}', script.string, re.DOTALL)
                if data_layer_info:
                    data_layer_info = data_layer_info.group(1)
                    data_layer_info = data_layer_info.replace("'", "\"")
                    data_layer_info = '{' + data_layer_info + '}'  
                    data_layer_info = eval(data_layer_info)

                    publication_data["propery_type"] = data_layer_info["propertyType"]
                    publication_data["listing_category"] = data_layer_info["listingCategory"]
                    publication_data["operation_type"] = data_layer_info["operationType"]
                    publication_data["city_datalayer_info"] = data_layer_info["city"]
                    publication_data["rental_price"] = data_layer_info["rentalPrice"]
                else:
                    publication_data["propery_type"] = None
                    publication_data["listing_category"] = None
                    publication_data["operation_type"] = None
                    publication_data["city_datalayer_info"] = None
                    publication_data["rental_price"] = None


# Esta es la antiguedad de la publicacion
                match = re.search(r"antiquity\s*=\s*\'(.*?)\'", script.string)
                if match:
                    antiquity_value = match.group(1)
                    publication_data["publication_antiquity"] = antiquity_value
                else:
                    publication_data["publication_antiquity"] = None

# Esto es la cantidad de visitas en los últimos treinta días, me sirve para estimar el interés que la publicación genera.
                visits = re.search(r"usersViews\s*=\s*(\d+)\b", script.string)
                if visits:
                    visits = visits.group(1)
                    publication_data["publication_visits_l30d"] = visits
                else:
                    publication_data["publication_visits_l30d"] = None

                general_features = re.search(r"'generalFeatures': (\{.*?\}\}\},)", script.string, re.DOTALL)
                if general_features:
                    # Extract the matched JSON string
                    general_features = general_features.group(1)
                    general_features = general_features[1:]
                    general_features = general_features[:-1]
                    general_features.replace("}}},","}}}}")
                    general_features = '{'+ general_features
                    general_features = re.sub(r"}}},", "}}}", general_features)
                    if len(general_features) > 2000:
                        general_features_dic = {}
                    else:
                        general_features_dic= json.loads(general_features)

                    checker = str(general_features_dic)

                    if "Ambientes" in checker:
                        ambientes_dic = general_features_dic["Ambientes"]
                    else:
                        ambientes_dic = {}
                    if "'Características' :" in checker:
                        try:
                            caracteristicas_dic = general_features_dic["Características"]
                        except Exception as e:
                            print(f'Error: {e}')
                            caracteristicas_dic = {}
                    else:
                        caracteristicas_dic = {}
                    if "Servicios" in checker:
                        servicios_dic = general_features_dic["Servicios"]
                    else: 
                        servicios_dic = {}

                    ambientes = []
                    for key, value in ambientes_dic.items():
                        ambiente = value['label']
                        ambientes.append(ambiente)
                    publication_data["ambientes"] = ambientes

                    servicios_dic.update(caracteristicas_dic)


                    servicios = []
                    for key, value in servicios_dic.items():
                        servicio = value['label']
                        servicios.append(servicio)


                wpp = re.search(r"'whatsApp':\s*'(\d{2,3}(\s?\d{1,4}){3,4})'\s*,", script.string) 
                if wpp:
                    phone_number = wpp.group(1)
                    phone_number = phone_number.replace(' ', '')
                    publication_data["publisher_whatsapp"] = phone_number
                else:
                    publication_data["publisher_whatsapp"] = None

                publication_date = re.search(r"'publicationDateFormatted':\s*'(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}(?::\d{2})?Z)'", script.string)
                if publication_date:
                    publication_date = publication_date.group(1)
                    if publication_date.endswith("Z") and len(publication_date.split("T")[1]) == 6:
                        publication_date = publication_date.replace("Z", ":00Z")
                    dt_object = datetime.datetime.strptime(publication_date, "%Y-%m-%dT%H:%M:%SZ")
                    publication_date = dt_object.strftime("%Y-%m-%d %H:%M:%S")
                    publication_data["publication_date"] = publication_date

                publisher_data_pattern = r"""
                    'publisherId':\s*'([^']*)', 
                    .*?'name':\s*'([^']*)',?
                    .*?'url':\s*'([^']*)',?
                    .*?'premium':\s*(true|false|null),?
                    .*?'publisherTypeId':\s*([\dnull]+),?
                """

                publisher_data = re.findall(publisher_data_pattern, script.string, re.DOTALL | re.VERBOSE)
                if publication_data:
                    for publisher_id, name, url, premium, publisher_type_id in publisher_data:
                        publication_data["publisher_id"] = publisher_id
                        publication_data["publisher_name"] = name
                        publication_data["publisher_url"] = url
                        publication_data["publisher_premium"] = premium
                        if publication_data["publisher_premium"] == 'false':
                            publication_data["publisher_premium"] = 0
                        elif publication_data["publisher_premium"] == 'true':
                            publication_data["publisher_premium"] = 1
                        publication_data["publisher_type_id"] = publisher_type_id
                else:
                    publication_data["publisher_id"] = None
                    publication_data["publisher_name"] = None
                    publication_data["publisher_url"] = None
                    publication_data["publisher_premium"] = None
                    publication_data["publisher_type_id"] = None

                main_features = re.search(r"'mainFeatures': (\{.*?\}\},)\n", script.string, re.DOTALL)

                publication_data['disposicion'] = None
                publication_data['orientacion'] = None
                publication_data['luminosidad'] = None
                publication_data['antiguedad'] = None
                publication_data['scubierta'] = None
                publication_data['stotal'] = None

                features = []
                if main_features:
                    # Extract the matched JSON string
                    main_features_json = main_features.group(1)
                    main_features_json = main_features_json[1:]
                    main_features_json = main_features_json[:-1]
                    main_features_json = '{'+ main_features_json
                    main_features_json = re.sub(r"}},", "}}", main_features_json)
                    main_features_dic = json.loads(main_features_json)
                    for key, value in main_features_dic.items():
                        if value['icon'] == 'ambiente':
                            continue
                        else:
                            publication_data[value["icon"]] = value["value"]
                            features.append(value["icon"])

                if publication_data['latitude'] is not None:
                    print(publication_data)
                    statement = f"""
                            UPDATE 
                                {self.dbtable}
                            SET
                                latitud = %s, 
                                longitud = %s, 
                                fecha_publicacion = %s, 
                                antiguedad_publicacion = %s,
                                visitas_u30d = %s,
                                superficie_total = %s,
                                superficie_cubierta = %s,
                                antiguedad = %s,
                                disposicion = %s,
                                orientacion = %s,
                                luminosidad = %s,
                                anunciante = %s,
                                anunciante_premium_si_o_no = %s,
                                anunciante_tipo_de_id = %s,
                                wpp_anunciante = %s,
                                url_anunciante = %s,
                                property_type = %s
                            WHERE 
                                id = {str(pub_id)};
                    """
                    publication_data_prepared = [publication_data['latitude'],
                                                 publication_data['longitude'],
                                                 publication_data['publication_date'],
                                                 publication_data['publication_antiquity'],
                                                 publication_data["publication_visits_l30d"],
                                                 publication_data['stotal'],
                                                 publication_data['scubierta'],
                                                 publication_data['antiguedad'],
                                                 publication_data['disposicion'],
                                                 publication_data['orientacion'],
                                                 publication_data['luminosidad'],
                                                 publication_data['publisher_name'],
                                                 publication_data['publisher_premium'],
                                                 publication_data['publisher_type_id'],
                                                 publication_data['publisher_whatsapp'],
                                                 publication_data['publisher_url'],
                                                 publication_data['propery_type']]
                                                

                    # Ahora hay que cargar los datos a la base de datos
                    try:
                        cur.execute(statement, publication_data_prepared)
                        conn.commit()
                    except Exception as e:
                        print(f"Error! :   {e}")
                    break

    def expand_data_multi(self, number_of_workers):

        conn = mysql.connector.connect(host="127.0.0.1", port=3306, user="Juancito", password="0223", database="ZonaProp_db", charset="utf8mb4", collation="utf8mb4_general_ci")
        cur = conn.cursor() 

        cur.execute(
                f'''
                SELECT
                    MAX(id)
                FROM
                    {self.dbtable};
                '''
                ) # Al tratarse de que el id es la primary key que se auto-aumenta a medida que se agregan publicaciones, el maximo es el total.

        number_of_pubs: int
        fetched: tuple
        fetched = cur.fetchone()

        number_of_pubs = int(fetched[0])

        intervalo = math.ceil(number_of_pubs / number_of_workers)

        rango = list()
        count = 0
        ultimo_rango = 1
        for i in range(1, number_of_workers + 1):
            count +=1
            if intervalo * i > number_of_pubs:
                rango.append(range(ultimo_rango, number_of_pubs + 1))
            else:
                rango.append(range(ultimo_rango, intervalo * i + 1))
                # Estos rangos son lo que le corresponde a cada worker.
            ultimo_rango = ultimo_rango + intervalo

        with concurrent.futures.ProcessPoolExecutor() as executor:
            executor.map(self.expand_data, rango)
