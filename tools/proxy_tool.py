import re
import cloudscraper
import requests
from itertools import cycle
import random

class ProxyList:
    def __init__(self, link):
        self.link = link 
        self.proxies_list = list()
        self.res = requests.get(self.link).text.splitlines()
        print('Getting proxies...')
        
        for proxy in self.res:
            proxies = dict()
            method = re.search('^[^:]+', proxy).group()
            if method == 'socks4':
                continue
            proxies[method] = proxy

            self.proxies_list.append(proxies)


        self.proxy_pool = self.proxies_list
        self.lap_count: int = 0
        self.pool_size: int = len(self.proxies_list)
        print('Proxy pool size: %s'% self.pool_size)

    def get_proxy(self):
        aProxy = random.choice(self.proxy_pool)
        print(f'Proxy usada:  {aProxy}')
        self.lap_count =+1
        if self.lap_count >= self.pool_size:
            print('All proxies have been used')
            self.lap_count = 0
        return aProxy




'''
def getting_proxies(a):
    res = requests.get(a).text.splitlines()
    proxies_list = list()
    for i in res:
        proxies = dict()
        method = re.search('^[^:]+', i).group()
        if method == 'socks4':
            continue
        proxi = i
        proxies[method] = proxi
        proxies_list.append(proxies)
    print(f'Cantidad de proxies disponibles: {len(proxies_list)}')
    return proxies_list
'''
