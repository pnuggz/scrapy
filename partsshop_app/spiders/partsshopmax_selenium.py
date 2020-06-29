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
        )), callback='parse_result', follow=True),
    )


    def parse_result(self, response):
        global urls
        if response.url.endswith('.html'):
            urls.append(response.url)


    def process_selenium(self):
        global urls
        driver = webdriver.Chrome("C:/Users/Ryan/Dev/scrapy/partsshop_app/chromedriver.exe")

        for url in urls:
            print(url)
            driver.get(url)
            time.sleep(5)

            # Get item title
            title = driver.find_element_by_xpath("//meta[@property='og:title']").get_attribute("content")
            # Get item description
            description = driver.find_element_by_xpath("//meta[@property='og:description']").get_attribute("content")
            # Get item price
            price = driver.find_element_by_xpath("//meta[@itemprop='price']").get_attribute("content")
            # Get item price currency
            price_currency = driver.find_element_by_xpath("//meta[@itemprop='priceCurrency']").get_attribute("content")
            # Get price EURO currency
            try:      
                price_euro = driver.find_element_by_xpath("//span[@class='price eudprice eudRemoveIfNotCarried']").text
            except:
                price_euro = None
            # Get price TWD currency
            try:
                price_twd = driver.find_element_by_xpath("//span[@class='price twdprice twdRemoveIfNotCarried']").text
            except:
                price_twd = None
            # Get price JPY currency        
            try:
                price_jpy = driver.find_element_by_xpath("//span[@class='price jpdprice jpdRemoveIfNotCarried']").text
            except:
                price_jpy = None
            # Get item in stock   
            stock_levels = driver.find_element_by_xpath("//button[@class='postfix item-qty-btn half-margin-top']/following-sibling::small").text
            # Get item in stock   
            stock_levels_twd = driver.find_element_by_xpath("//form[@id='add-cart-form'][2]/div/div[2]/small").text      
            # Get item SKU
            sku = driver.find_element_by_xpath("//meta[@itemprop='productID']").get_attribute('content')

            item = OrderedDict()
            item['url'] = url
            item['title'] = title
            item['description'] = description
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


    def closed(self, reason):
        self.process_selenium()    
 