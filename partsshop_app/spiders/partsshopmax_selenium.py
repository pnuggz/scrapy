# -*- coding: utf-8 -*-
import scrapy
from scrapy_selenium import SeleniumRequest
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from collections import OrderedDict
from selenium import webdriver
import time

urls = []

class PartsshopmaxSeleniumSpider(CrawlSpider):
    name = 'partsshopmax_selenium'
    allowed_domains = ['store.partsshopmax.com']
    start_urls = ['https://store.partsshopmax.com/']
   

    rules = (
        Rule(LinkExtractor(
            allow=(
                r'/shop/silvia/\w+/', 
                # include more categories here, if new category added in future
        )), callback='parse_request', follow=True),
    )
       
    
    def parse_request(self, response):      
        if response.url.endswith('.html'):
            # Get item title
            title = response.xpath("//meta[@property='og:title']/@content").extract_first()
            # Get item description
            description = response.xpath("//section[@id='panel-product-description']/article/div/text()").extract_first()
            # Get item price
            price = response.xpath("//meta[@itemprop='price']/@content").extract_first()
            # Get item price currency
            price_currency = response.xpath("//meta[@itemprop='priceCurrency']/@content").extract_first()
            # Get price EURO currency        
            price_euro = response.xpath("normalize-space(//span[@class='price eudprice eudRemoveIfNotCarried']/text()[2])").get()
            # Get price TWD currency        
            price_twd = response.xpath("normalize-space(//span[@class='price twdprice twdRemoveIfNotCarried']/text()[2])").get()
            # Get price JPY currency        
            price_jpy = response.xpath("normalize-space(//span[@class='price jpdprice jpdRemoveIfNotCarried']/text()[2])").get()
            # Get item in stock   
            stock_levels = response.xpath("//button[@class='postfix item-qty-btn half-margin-top']/following-sibling::small/text()").extract_first()
            # Get item in stock   
            stock_levels_twd = response.xpath("//form[@id='add-cart-form'][2]/div/div[2]/small/text()[2]").extract_first()          
            # Get item SKU
            sku = response.xpath("//meta[@itemprop='productID']/@content").extract_first()

            item = OrderedDict()
            #item['url'] = response.url
            #item['title'] = title
            #item['description'] = description
            item['price'] = '{0} {1}'.format(price, price_currency)
            item['price_euro'] = price_euro
            item['price_twd'] = price_twd
            item['price_jpy'] = price_jpy
            item['stock_levels'] = stock_levels.strip() if stock_levels else 'Not listed'
            item['stock_levels_twd'] = stock_levels_twd
            item['sku'] = sku
            print('')
            print(item)
            print('')
            yield item