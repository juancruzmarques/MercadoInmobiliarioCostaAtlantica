from tools.proxy_tool import ProxyList
from tools.scraper_tool import Scraper

api_proxies=  "https://api.proxyscrape.com/v4/free-proxy-list/get?request=display_proxies&country=ar&proxy_format=protocolipport&format=text" 
link = "https://www.zonaprop.com.ar/departamentos-venta-buenos-aires-costa-atlantica.html"

def main():
    proxy = ProxyList(api_proxies)
    busqueda = Scraper(link, proxy)
    busqueda.get_pubs()

if __name__ == '__main__':
    main()
