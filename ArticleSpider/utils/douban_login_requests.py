import requests

try:
    import cookielib
except:
    import http.cookiejar as cookielib
import re

session = requests.session()
session.cookies = cookielib.LWPCookieJar(filename="cookies.txt")
try:
    session.cookies.load(ignore_discard=True)
    print("cookie已经加载")
except:
    print("cookie未能加载")

# Mozilla/5.0
# agent = "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0"
agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0"
# Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0
header2 = {
    "HOST": "www.zhihu.com",
    "Referer": "https://www.zhizhu.com/signin",
    'User-Agent': agent
}

header = {
    "HOST": "accounts.douban.com",
    # https://www.douban.com/accounts/login?redir=https%3A//accounts.douban.com/
    "Referer": "https://www.douban.com/accounts/login?source=movie",
    'User-Agent': agent
}


def is_login():
    # 通过个人中心页面返回状态码来判断是否为登录状态，如果未登录返回302，跳转到登录页面后返回200
    # 已经登录直接返回200
    inbox_url = "https://www.douban.com/people/72897457/"
    # inbox_url = "https://www.douban.com/"
    response = session.get(inbox_url, allow_redirects=False)  # 允许重定向设置为False
    if response.status_code != 200:
        return False
    else:
        return True

def get_captcha():
    import time
    t = str(int(time.time()*1000))
    captcha_url = "https://www.zhihu.com/captcha.gif?r={0}&type=login".format(t)
    t = session.get(captcha_url, headers=header)
    with open("captcha.jpg","wb") as f:
        f.write(t.content)
        f.close()

    from PIL import Image
    try:
        im = Image.open('captcha.jpg')
        im.show()
        im.close()
    except:
        pass

    captcha = input("输入验证码\n>")
    return captcha
def get_xsrf():
    # 获取xsrf code
    response = session.get("https://www.zhihu.com/api/v3/oauth/sign_in", headers=header)
    print(response.text)


# get_xsrf()



def douban_login(account, password):
    # 豆瓣登录
    post_url = "https://accounts.douban.com/login"
    post_data = {
        "form_email": account,
        "form_password": password
    }
    # response = requests.get("https://movie.douban.com/")
    response = session.post(post_url, data=post_data)
    with open("douban.html", "wb") as f:
        f.write(response.text.encode("utf-8"))
    # print(response.text)
    print(response.status_code)
    print(session.cookies)
    session.cookies.save()


douban_login("934008411@qq.com", "93zh09ao21")
print(is_login())
