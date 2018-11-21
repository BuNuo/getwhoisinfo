# -*- coding: utf-8 -*-
import scrapy


class AliyunSpider(scrapy.Spider):
    name = 'aliyun'
    # allowed_domains = ['aliyun.com']
    start_urls = ['https://whois.aliyun.com/whois/domain/skri.cn']

    def parse(self, response):
        self.logger.debug('--------------User-Agent----------------')
        self.logger.debug(response.request.headers['User-Agent'])
        self.logger.debug(response.request.meta['proxy'])
        node_list = response.xpath('//*[@id="info_whois"]/div[1]/span')

        print(node_list)
