# -*- coding: utf-8 -*-
import scrapy


class MlSpider(scrapy.Spider):
    name = 'ml'
    allowed_domains = ['mercadolivre.com.br']
    start_urls = ['http://mercadolivre.com.br/']

    def start_requests(self):
    	for url in start_urls:
    		yeild scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = 'quotes-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)
