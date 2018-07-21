# -*- coding: utf-8 -*-
import scrapy
from selenium import webdriver
import codecs,os


class ZhihuSelSpider(scrapy.Spider):
    name = 'zhihu_sel'
    allowed_domains = ['www.zhihu.com']
    start_urls = ['http://www.zhihu.com/']

    def parse(self, response):
        pass

    def parse_question(self, response):
        pass

    def parse_answer(self, response):
        pass

    def start_requests(self):
        # selenium动态网页请求与模拟登陆知乎
        browser = webdriver.Chrome(
            # executable_path="C:/Users/a9340/Downloads/geckodriver-v0.21.0-win64/geckodriver.exe")
            executable_path="C:/Users/a9340/Downloads/chromedriver.exe")

        # browser.get("https://www.liaoxuefeng.com/wiki/0013739516305929606dd18361248578c67b8067c8c017b000/0013760174128707b935b0be6fc4fc6ace66c4f15618f8d000")
        browser.get("https://www.zhihu.com/signin")
        # 模拟输入账户名和密码
        browser.find_element_by_css_selector(".SignFlow-accountInput input[name='username']").send_keys(
            "934008411@qq.com")
        browser.find_element_by_css_selector(".SignFlow-password input[name='password']").send_keys("93zh09ao21")
        # 模拟点击登录操作
        browser.find_element_by_css_selector("button.SignFlow-submitButton").click()
        import time
        time.sleep(10)
        # 延时10s后拿到cookies
        cookies = browser.get_cookies()
        # print(cookies)
        cookie_dict = {}
        import pickle
        project_dir = os.path.abspath(os.path.dirname(__file__))
        cookie_path = os.path.join(project_dir, 'zhihu\\')
        for cookie in cookies:
            # 写入文件
            f = codecs.open(cookie_path + cookie['name'] + '.zhihu', 'wb')
            pickle.dump(cookie, f)
            f.close()
            cookie_dict[cookie['name']] = cookie['value']
        # print(cookie_dict)
        browser.close()
        return [scrapy.Request(url=self.start_urls[0], dont_filter=True, cookies=cookie_dict)]

