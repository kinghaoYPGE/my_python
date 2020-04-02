# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from louspider.items import LouspiderItem

class MylouspiderSpider(scrapy.Spider):
    name = 'louspider'
    allowed_domains = ['shiyanlou.com']
    start_urls = ['https://www.shiyanlou.com/courses/?category=all&course_type=all&tag=all&fee=free']
    def parse(self, response):
        print('=====scrapy fetch start=====')
        html = Selector(response)
        courses = html.xpath('//div[@class="col-md-3 col-sm-6  course"]')
        
        for course in courses:
            item = LouspiderItem()
            item['name'] = course.xpath('.//div[@class="course-name"]/text()').extract_first().strip()
            item['image'] = course.xpath('.//div[@class="course-img"]/img/@src').extract_first().strip()
            item['learned'] = course.xpath('.//span[@class="course-per-num pull-left"]/text()').extract_first().strip()

            yield item
            

        next_url = html.xpath('//a[@aria-label="Next"]/@href').extract_first()
        #处理是否有下一页
        if next_url:
            print('====fetch next url %s==='%next_url)
            yield scrapy.Request('https://www.shiyanlou.com'+next_url, callback=self.parse)