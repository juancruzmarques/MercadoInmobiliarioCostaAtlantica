from tools import ProxyList, Scraper
import time

api_proxies=  "https://api.proxyscrape.com/v4/free-proxy-list/get?request=display_proxies&country=ar&proxy_format=protocolipport&format=text" 
link = "https://www.zonaprop.com.ar/departamentos-venta-buenos-aires-costa-atlantica.html"

def main():
    hilos = input('¿Cuantos procesos concuerrentes desea realizar? :')
    if hilos is not int: #Validamos la opción de lo contrario colocamos 1 como la cantidad de subprocesos a crear.
        hilos = 1
    else:
        hilos = int(hilos)

    exclusivo_expandir = input('¿Desea exclusivamente realizar la expansión? (s/n):')

    start_time = time.time()

    proxy = ProxyList(api_proxies)
    busqueda = Scraper(link, proxy, 'Propiedades6')

    # Si solo queremos expandir los datos entrando a cada link.
    if exclusivo_expandir in ['n', 'N']:
        expandir = input('¿Desea expandir los datos al finalizar la busqueda inicial? (s/n):')
        if expandir not in ['s', 'n', 'S', 'N']: # Validamos la opción
            expandir = 'n'
        busqueda.get_pubs_multi(hilos) #scrapeo
        if expandir in ['s', 'S']:
            busqueda.expand_data_multi(hilos)
    else:
       pass 

    end_time = time.time()
    elapsed_time = end_time - start_time

    if elapsed_time < 60:
        print(f"Script executed in {elapsed_time:.2f} seconds.")
    else:
        print(f"Script executed in {elapsed_time / 60:.2f} minutes.")

if __name__ == '__main__':
    main()
