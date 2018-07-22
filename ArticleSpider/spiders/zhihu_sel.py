# -*- coding: utf-8 -*-
import scrapy
from selenium import webdriver
import codecs, os
from urllib import parse




class ZhihuSelSpider(scrapy.Spider):
    name = 'zhihu_sel'
    allowed_domains = ['www.zhihu.com']
    start_urls = ['http://www.zhihu.com/']

    #question的第一页answer的请求url
    start_answer_url = "https://www.zhihu.com/api/v4/questions/29372574/answers?data%5B%2A%5D.author.follower_count%2Cbadge%5B%3F%28type=best_answerer%29%5D.topics&data%5B%2A%5D.mark_infos%5B%2A%5D.url=&include=data%5B%2A%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Crelevant_info%2Cquestion%2Cexcerpt%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp&limit=5&offset=0&sort_by=default"

    agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.68 Safari/537.36"
    headers = {
    "HOST": "www.zhihu.com",
    "Referer": "https://www.zhihu.com",
    "User-Agent": agent
    }

    # scrapy shell -s USER_AGENT="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.68 Safari/537.36" https://www.zhihu.com/question/56320032

    def parse(self, response):
        # pass
        # 提取出html页面中的所有url，并跟踪这些url进一步爬取
        # 如果提取的url中格式为/question/xxx 就下载之后直接进入解析函数
        # all_urls = response.css("a::attr(href)").extract()
        # all_urls = [parse.urljoin(response.url,url) for url in all_urls]
        # for url in all_urls:


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
        return [scrapy.Request(url=self.start_urls[0], headers=self.headers, dont_filter=True, cookies=cookie_dict)]
