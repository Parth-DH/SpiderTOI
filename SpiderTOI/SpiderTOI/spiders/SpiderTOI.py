#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 17 04:18:21 2018

@author: parth
"""

#This crawler is made for finding HIV related articles of 2009 and 2010 from TOI

import scrapy

class Item1(scrapy.Item):
	Title = scrapy.Field()
	Date = scrapy.Field()
	article = scrapy.Field()
    
class SpiderTOI(scrapy.Spider):
    name = 'SpiderTOI'
    keyword = 'HIV'

    
    def start_requests(self):
        #39814 --> starttime for Jan 01 2009
        #40543 --> starttime for Dec 31 2010
        urls = ['https://timesofindia.indiatimes.com/archivelist/starttime-%d.cms' % x for x in range(39814,40543)]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parsekey)
        
        
    def parsekey(self, response):
        foundArticle = response.xpath('//span/a[contains(text(), "'+self.keyword+'")]')
        foundLink = foundArticle.xpath('@href').extract()
        for link in foundLink:
            yield scrapy.Request(response.urljoin(link), callback=self.parse)
            
    def parse(self, response):
        item = Item1()
        item['Title'] = response.xpath('//section/h1/text()').extract()
        item['Date'] = response.xpath('//section/span/span/text()').extract()
        item['article'] = response.xpath('//arttextxml/text()').extract()
        yield item
        
        
