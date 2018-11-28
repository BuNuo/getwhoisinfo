# -*- coding: utf-8 -*-
import scrapy
import js2xml
from lxml import etree
from bs4 import BeautifulSoup
from js2xml.utils.vars import get_vars
import requests



class AliyunSpider(scrapy.Spider):
    name = 'aliyun'
    # allowed_domains = ['aliyun.com']
    start_urls = ['https://whois.aliyun.com/whois/domain/skriiiiiii.cn']



    def parse(self, response):
        self.logger.debug('--------------User-Agent----------------')
        self.logger.debug(response.request.headers['User-Agent'])
        self.logger.debug(response.request.meta['proxy'])
        # node_list = response.xpath('//*[@id="info_whois"]/div[1]/span')
        # print(node_list)

        snippet = response.css('script:contains("umToken")::text').get()
        src_text = js2xml.parse(snippet, encoding='utf-8', debug=False)
        src_tree = js2xml.pretty_print(src_text)
        selector = etree.HTML(src_tree)
        umToken = selector.xpath("//var[@name = 'umToken']/string/text()")[0]


        yield scrapy.Request('https://whois.aliyun.com/whois/api_whois?host=skriiiiiii.cn&umToken='+umToken,
                             headers={
                                 'User-Agent': response.request.headers['User-Agent']
                             },
                             cookies=response.request.cookies,
                             callback=self.parse2)

    def parse2(self, response):
        print(response.text)




