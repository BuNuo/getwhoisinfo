# -*- coding: utf-8 -*-
# author  : bunuo
# datetime   : 2018/11/20 13:47
# filename   : get_ip_agent.py


from bs4 import BeautifulSoup
import requests
import random
import telnetlib

def get_ip_status(ip,port):
    server = telnetlib.Telnet()
    result = False
    try:
        server.open(ip,port,15)
        result = True
        print('{0} port {1} is open'.format(ip, port))
    except Exception as err:
        print('{0} port {1} is not open'.format(ip,port))
    finally:
        server.close()

    return result

def get_ip_list(url, proxies, headers):
    web_data = requests.get(url, proxies=proxies, headers=headers)
    soup = BeautifulSoup(web_data.text, 'lxml')
    ips = soup.find_all('tr')
    ip_list = []
    for i in range(1, len(ips)):
        ip_info = ips[i]
        tds = ip_info.find_all('td')
        country = tds[0]
        area = tds[3]
        protocol = tds[5]
        speed = tds[6]
        linkDate = tds[7]
        existDate = tds[8]

        if not len(country) != 0:
            continue

        # if area.find('a').text != '北京':
        #     continue

        if not speed.find(attrs={"class":"bar_inner fast"}):
            continue

        if not linkDate.find(attrs={"class":"bar_inner fast"}):
            continue

        speedDiv = speed.find(attrs={"class":"bar_inner fast"})
        if speedDiv.has_attr('style'):
            spd = speedDiv.get('style').split(':')[1].strip('%') #速度
            if '天' in existDate.text:
                exd = existDate.text.strip('天')
                if int(exd) >= 100 and int(spd) >= 10:
                    if get_ip_status(tds[1].text, tds[2].text):
                        ip_list.append(protocol.text.lower() + '://' + tds[1].text + ':' + tds[2].text)
    return ip_list

def get_random_ip(ip_list):
    proxy_list = []
    for ip in ip_list:
        proxy_list.append(ip)
    proxy_ip = random.choice(proxy_list)
    proxies = {'http': proxy_ip}
    return proxies

def sendRequest(page):
    print(page)
    url = 'http://www.xicidaili.com/nn/' + str(page)
    proxies = {'http': 'http://119.29.241.209:808'}
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'
    }
    return get_ip_list(url, proxies=proxies,headers=headers)

if __name__ == '__main__':
    page = 1

    ip_list = []
    while not ip_list:
        ip_list = sendRequest(page)
        page+=1

    proxies = get_random_ip(ip_list)
    print(proxies)