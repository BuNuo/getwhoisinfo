# -*- coding: utf-8 -*-
import scrapy
import js2xml
import json
from getwhoisinfo.items import GetwhoisinfoItem
from lxml import etree



class AliyunSpider(scrapy.Spider):
    name = 'aliyun'
    allowed_domains = ['aliyun.com']
    domains = 'iou.com'
    start_urls = ['https://whois.aliyun.com/whois/domain/'+domains]



    def parse(self, response):
        self.logger.debug('--------------User-Agent----------------')
        self.logger.debug(response.request.headers['User-Agent'])
        self.logger.debug(response.request.meta['proxy'])

        snippet = response.css('script:contains("umToken")::text').get()
        src_text = js2xml.parse(snippet, encoding='utf-8', debug=False)
        src_tree = js2xml.pretty_print(src_text)
        selector = etree.HTML(src_tree)
        umToken = selector.xpath("//var[@name = 'umToken']/string/text()")[0]

        yield scrapy.Request('https://whois.aliyun.com/whois/api_whois?host=' + self.domains + '&umToken='+umToken,
                             headers={
                                 'User-Agent': response.request.headers['User-Agent']
                             },
                             cookies=response.request.cookies,
                             callback=self.parse2)

    def parse2(self, response):
        jsonObj = json.loads(response.text)
        #print(jsonObj)
        code = jsonObj['code']
        if code == '1000':
            item = GetwhoisinfoItem()
            module = jsonObj['module']
            print(module)
            registrantOrganization = module.get('registrantOrganization')
            registrar = module.get('registrar')
            standardFormatExpirationDate = module.get('standardFormatExpirationDate')
            registrarExpirationDateDayOfYearIntervals = module.get('registrarExpirationDateDayOfYearIntervals')
            registrantEmail = module.get('registrantEmail')
            formatExpirationDate = module.get('formatExpirationDate')
            formatCreationDate = module.get('formatCreationDate')
            statusInfos = module.get('statusInfos')
            expirationDate = module.get('expirationDate')
            creationDate = module.get('creationDate')
            print(expirationDate)
            print(statusInfos)





