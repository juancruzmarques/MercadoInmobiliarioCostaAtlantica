from tools.proxy_tool import ProxyList
from tools.scraper_tool import Scraper
import time

api_proxies=  "https://api.proxyscrape.com/v4/free-proxy-list/get?request=display_proxies&country=ar&proxy_format=protocolipport&format=text" 
link = "https://www.zonaprop.com.ar/departamentos-venta-buenos-aires-costa-atlantica.html"


def main():
    start_time = time.time()
    proxy = ProxyList(api_proxies)
    busqueda = Scraper(link, proxy)
    #busqueda.get_pubs()
    busqueda.get_pubs_multi(3)
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Script executed in {elapsed_time:.2f} seconds.")

if __name__ == '__main__':
    main()
