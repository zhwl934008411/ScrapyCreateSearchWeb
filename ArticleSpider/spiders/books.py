# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from urllib import parse


class BooksSpider(scrapy.Spider):
    name = 'books'
    start_urls = ['http://books.toscrape.com/']

    def parse(self, response):
        for book in response.css("article.product_pod"):
            name = book.css("h3 a::text").extract_first()
            price = book.css(".product_price .price_color::text").extract_first()
            yield {
                'name': name,
                'price': price,
            }
        nextpage = response.css('ul.pager li.next a::attr(href)').extract_first()
        if nextpage:
            #nextPage = response.urljoin(nextPage)
            #yield scrapy.Request(nextPage, callback=self.parse)
            nextpage2 = parse.urljoin(response.url, nextpage)
            yield Request(url=nextpage2, callback=self.parse)


