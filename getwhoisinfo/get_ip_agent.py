# -*- coding: utf-8 -*-
# author  : bunuo
# datetime   : 2018/11/20 13:47
# filename   : get_ip_agent.py


from bs4 import BeautifulSoup
import requests
import random

def get_ip_list(url, headers):
    web_data = requests.get(url, headers=headers)
    soup = BeautifulSoup(web_data.text, 'lxml')
    ips = soup.find_all('tr')
    ip_list = []
    for i in range(1, len(ips)):
        ip_info = ips[i]
        tds = ip_info.find_all('td')
        country = tds[0]
        protocol = tds[5]
        speed = tds[6]
        if len(country) != 0 and speed.find(attrs={"class":"bar_inner fast"}) :
            ip_list.append(protocol.text.lower() + '://' + tds[1].text + ':' + tds[2].text)
    return ip_list

def get_random_ip(ip_list):
    proxy_list = []
    for ip in ip_list:
        proxy_list.append(ip)
    proxy_ip = random.choice(proxy_list)
    proxies = {'http': proxy_ip}
    return proxies

if __name__ == '__main__':
    page = random.randint(2, 100)
    url = 'http://www.xicidaili.com/nn/'+ str(page)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'
    }
    ip_list = get_ip_list(url, headers=headers)
    proxies = get_random_ip(ip_list)
    print(proxies)
