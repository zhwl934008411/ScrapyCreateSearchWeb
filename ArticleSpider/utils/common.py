import hashlib


def get_md5(url):
    if isinstance(url,str):
        url = url.encode("utf8")
    m = hashlib.md5()
    m.update(url)
    return m.hexdigest()


if __name__ == '__main__':
    x = get_md5("https://coding.imooc.com/lesson/92.html#mid=2878")
    print(len(x))  # 转化为一个定长为32的值
