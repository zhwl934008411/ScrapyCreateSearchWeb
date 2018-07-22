# -*- coding: utf-8 -*-
import scrapy
from scrapy import FormRequest
import json


class DoubanSpider(scrapy.Spider):
    name = 'douban'
    allowed_domains = ['wwww.douban.com']
    start_urls = ['http://www.douban.com/']
    agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0"
    headers = {
        "HOST": "accounts.douban.com",
        # https://www.douban.com/accounts/login?redir=https%3A//accounts.douban.com/
        "Referer": "https://accounts.douban.com/login",
        'User-Agent': agent
    }

    def parse(self, response):
        pass

    def start_requests(self):
        return [scrapy.Request("https://accounts.douban.com/login", headers=self.headers, callback=self.douban_login)]

    def douban_login(self, response):
        response_text = response.text
        # response.text
        post_url = "https://accounts.douban.com/login"
        post_data = {
            "form_email": "934008411@qq.com",
            "form_password": "93zh09ao21f"
        }
        hh = FormRequest(
            url=post_url,
            formdata=post_data,
            callback=self.check_login
        )
        # 登录操作
        return [hh]

    def check_login(self, response):
        # 验证服务器的返回数据判断是否成功
        # print(response.text)
        text_json = json.load(response.text)
        if "msg" in text_json and text_json["msg"] == "登陆成功":
            for url in self.start_urls:
                yield scrapy.Request(url,dont_filter=True,headers=self.headers)
                yield self.make_requests_from_url(url)

