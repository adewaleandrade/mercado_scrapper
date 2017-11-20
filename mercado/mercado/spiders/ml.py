# -*- coding: utf-8 -*-
import scrapy
import base64

class MlSpider(scrapy.Spider):
    name = 'ml'
    allowed_domains = ['mercadolivre.com.br']

    url_categories = {
    	'https://tenis.mercadolivre.com.br/masculino/tenis-masculino': 'tenis',
    	'https://roupas.mercadolivre.com.br/vestidos/feminino/': 'roupas',
    	'https://tenis.mercadolivre.com.br/feminino/tenis-feminino': 'tenis',
    	'https://roupas.mercadolivre.com.br/calcados-roupas/roupas-femininas': 'roupas',
    	'https://roupas.mercadolivre.com.br/camisetas-blusas/camisetas-blusas_9993122-AMLB*3122*2_9993122-AMLB*3122*2-MMLB33286': 'roupas',
    	'https://celulares.mercadolivre.com.br/': 'celular' ,
    	'https://roupas.mercadolivre.com.br/calcados-roupas/sandalias-femininas': 'roupas',
    	'https://relogios.mercadolivre.com.br/pulso/': 'relogios',
    	'https://lista.mercadolivre.com.br/esportes-aventura-e-acao-armas-propulsao/airsoft': 'airsoft',
    	'https://lista.mercadolivre.com.br/pisos-paredes-e-esquadrias/revestimento-parede/papel-parede': 'decoracao'
    }

    start_urls = list(url_categories.keys())
    currentCategory = url_categories[list(url_categories.keys())[0]]


    def start_requests(self):
    	for url in self.start_urls:
    		yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        items = response.css("li.results-item")
        for item in items:
            item = item.css("a.item__info-link")
            salesField = item.css(".item__status div.item__condition::text").extract_first()
            if salesField is None:
                continue

            sales = [int(s) for s in salesField.split() if s.isdigit()]
            if not sales:
            	continue

            sales = sales[0]
            url =  item.css('::attr(href)').extract_first()
            category = self.currentCategory
            if response.url in self.start_urls:
            	category = self.url_categories[response.url]

            base64Id = base64.b64encode(bytes(url, 'utf-8'))
            listing = {
            	'id': base64Id,
                'title': item.css(".item__title span.main-title::text").extract_first(),
                'url': url,
                'price': item.css(".item__price span.price-fraction::text").extract_first(),
                'reviews': item.css(".item__reviews div.item__reviews-total::text").extract_first(),
                'sales': sales,
                'category': category 
            }
            yield listing

        next_page = response.css(".pagination__container li.pagination__next a::attr(href)").extract_first()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
