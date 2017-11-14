# -*- coding: utf-8 -*-
import scrapy


class MlSpider(scrapy.Spider):
    name = 'ml'
    allowed_domains = ['mercadolivre.com.br']
    start_urls = ['http://mercadolivre.com.br/']

    def start_requests(self):
    	for url in self.start_urls:
    		yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        items = response.css("li.results-item")
        for item in items:
            item = item.css("a.item__info-link").extract_first()
            salesField = item.css(".item__status div.item__condition::text").extract_first()
            if (!salesField) :
                continue
            listing = {
                'url': item.css('a.item_info-link::attr(href)').extract_first(),
                'title': item.css(".item__title span.main-title::text").extract_first(),
                'price': item.css(".item__price span.price-fraction::text").extract_first(),
                'reviews': item.css(".item__reviews div.item__reviews-total::text").extract_first(),
                'sales': [int(s) for s in salesField.split() if s.isdigit()][0]
            }
            print listing
            exit

