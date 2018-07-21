# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy,re
from datetime import datetime
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst, Join


# Mapcompose可以传入函数对于该字段进行处理，而且可以传入多个


class ArticlespiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


def add_jobbole(value):
    return value + "-jobbole"


def date_convert(value):
    # createdate2 = re.sub('\r|\n| |·', '', response.css(".entry-meta-hide-on-mobile::text").extract()[0])
    try:
        createdate = datetime.strptime(value, '%Y/%m/%d').date()
    except Exception as e:
        createdate = datetime.now().date()
    return createdate


def get_nums(value):
    m3 = re.search(r'\d+', value)
    if m3:
        nums = int(m3.group(0))
    else:
        nums = 0
    return nums


def remove_comment_tags(value):
    if "评论" in value:
        # return value.replace("评论", "")
        return ""
    else:
        return value


def return_value(value):
    return value


class ArticleItemLoader(ItemLoader):
    # 自定义itemloader实现默认提取第一个
    default_output_processor = TakeFirst()


class JobBoleArticleItem(scrapy.Item):
    title = scrapy.Field(
        # input_processor = Mapcompose(lambda x:x+"-jobbole",add_jobbole)
    )
    createdate = scrapy.Field(
        input_processor=MapCompose(date_convert),
        # output_processor=TakeFirst()
    )
    url = scrapy.Field()
    url_object_id = scrapy.Field()  # 对url进行MD5转换为一个长度固定的值
    front_image_url = scrapy.Field(
        # List保持原值
        output_processor=MapCompose(return_value)
    )
    front_image_path = scrapy.Field()  # 存放image的路径
    thumbs = scrapy.Field(
        input_processor=MapCompose(get_nums)
    )
    bookmark = scrapy.Field(
        input_processor=MapCompose(get_nums)
    )
    comments = scrapy.Field(
        input_processor=MapCompose(get_nums)
    )
    contents = scrapy.Field()
    tags = scrapy.Field(
        input_processor=MapCompose(remove_comment_tags),
        output_processor=Join(",")
    )
    author = scrapy.Field()
