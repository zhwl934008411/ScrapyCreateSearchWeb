from selenium import webdriver
from scrapy.selector import Selector

# selenium动态网页请求与模拟登陆知乎
browser = webdriver.Firefox(executable_path="C:/Users/a9340/Downloads/geckodriver-v0.21.0-win64/geckodriver.exe")

# browser.get("https://www.liaoxuefeng.com/wiki/0013739516305929606dd18361248578c67b8067c8c017b000/0013760174128707b935b0be6fc4fc6ace66c4f15618f8d000")
browser.get("https://www.zhihu.com/signin")
# 模拟输入账户名和密码
browser.find_element_by_css_selector(".SignFlow-accountInput input[name='username']").send_keys("934008411@qq.com")
browser.find_element_by_css_selector(".SignFlow-password input[name='password']").send_keys("93zh09ao21")
# 模拟点击登录操作
browser.find_element_by_css_selector("button.SignFlow-submitButton").click()


# print(browser.page_source)

# t_selector = Selector(text=browser.page_source)
# title = t_selector.css(".x-content > h4:nth-child(1)::text").extract_first()

# print(title)

# ws NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0
# ws NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0
# browser.quit()