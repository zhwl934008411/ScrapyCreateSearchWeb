# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy.http import Request
from urllib import parse
from ArticleSpider.items import JobBoleArticleItem
from ArticleSpider.utils import common
# from datetime import datetime
# from scrapy.loader import Itemloader
from ArticleSpider.items import ArticleItemLoader



class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['blog.jobbole.com']
    # start_urls = ['http://blog.jobbole.com/110287']
    # start_urls = ['http://blog.jobbole.com']
    start_urls = ['http://blog.jobbole.com/all-posts/']

    def parse(self, response):
        """
        1.获取文章列表页中的文章url并交给scrapy下载后进行解析函数进行具体字段的解析
        2.获取下一页的URL并交给Scrapy进行下载，下载后返回给parse
        """
        # 解析列表页中的所有文章url并交给scrapy下载后进行解析,提取image url
        post_nodes = response.css("#archive .floated-thumb .post-thumb a")
        for post_node in post_nodes:
            image_url = post_node.css("img::attr(src)").extract_first()
            post_url = post_node.css("::attr(href)").extract_first()
            # parse.urljoin(respone.url,post_url)表示的是或的关系，
            # 如果post_url存在则url=post_url
            # 如果post_url不存在则url=response_url
            yield Request(url=parse.urljoin(response.url, post_url), meta={"front_image_url": image_url},
                          callback=self.parse_detail)
        # 提取下一页的URL并交给Scrapy进行下载，下载后返回给parse
        # 如果.next .pagenumber 是指两个class为层级关系。而不加空格为同一个标签
        next_url = response.css(".next.page-numbers::attr(href)").extract_first("")
        if next_url:
            yield Request(url=parse.urljoin(response.url, post_url), callback=self.parse)

    def parse_detail(self, response):
        article_item = JobBoleArticleItem()
        # 提取文章的具体字段，也属于回调函数
        '''#通过XPATH提取字段
        #获取标题
        response.xpath('//*[@id="post-110287"]/div[1]/h1/text()').extract_first()
        #获取时间
        createdate = re.sub('\r|\n| |·', '', response.xpath('//p[@class="entry-meta-hide-on-mobile"]/text()').extract()[0])
        #获取点赞数
        thumbs = int(response.xpath('//span[contains(@class,"vote-post-up")]/h10/text()').extract()[0])
        #获取收藏数
        bookmark = int(response.xpath('//span[contains(@class,"bookmark-btn")]/text()').extract()[0].split()[0])
        #获取评论数
        comments = int(response.xpath("//div[@class='post-adds']/a/span/text()").extract()[0].split()[0])
        #获取正文
        contents = response.xpath('//div[@class="entry"]').extract()
        #获取career
        career = response.xpath("//p[@class='entry-meta-hide-on-mobile']/a[1]/text()").extract()[0],\
                 response.xpath("//p[@class='entry-meta-hide-on-mobile']/a[3]/text()").extract()[0]
        career2 = response.xpath("//p[@class='entry-meta-hide-on-mobile']/a/text()").extract()
        career3 = [element for element in career2 if not element.strip().endswith("评论")]
        tags = ','.join(career3)
        #获取作者
        author =  response.xpath("//a[@href='http://www.jianshu.com/p/dc859753a035']/text()").extract_first()
        '''
        '''
        # 通过CSS选择器提取字段
        # 获取标题左侧图片,文章封面
        front_image_url = response.meta.get("front_image_url", "")
        # 获取标题
        title = response.css(".entry-header h1::text").extract()[0]
        # 获取时间
        createdate2 = re.sub('\r|\n| |·', '', response.css(".entry-meta-hide-on-mobile::text").extract()[0])
        try:
            createdate = datetime.strptime(createdate2, '%Y/%m/%d').date()
        except Exception as e:
            createdate = datetime.now().date()
        # 拿到url的md5值
        url_object_id = common.get_md5(response.url)
        # 获取点赞数
        m3 = re.search(r'\d+', response.css("span[class*='vote-post-up'] h10::text").extract_first())
        if m3:
            thumbs = int(m3.group(0))
        else:
            thumbs = None
        # 获取收藏数
        m1 = re.search(r'\d+', response.css("span[class*='bookmark-btn']::text").extract_first())
        if m1:
            bookmark = int(m1.group(0))
        else:
            bookmark = None
        # 获取评论数
        m2 = re.search(r'\d+', response.css("div.post-adds a span::text").extract_first())
        if m2:
            comments = int(m2.group(0))
        else:
            comments = None
        # 获取正文
        contents = response.css("div.entry").extract()
        # 获取career
        career = response.css("p.entry-meta-hide-on-mobile a::text").extract()
        career2 = [element for element in career if not element.strip().endswith("评论")]
        tags = ','.join(career2)
        # 获取作者
        author = response.css(".copyright-area > a::text").extract_first()
        # author = response.css(".copyright-area a:nth-child(1)::text").extract_first()


        article_item["title"] = title
        article_item["createdate"] = createdate
        article_item["url"] = response.url
        article_item["url_object_id"] = url_object_id
        article_item["front_image_url"] = [front_image_url]
        article_item["thumbs"] = thumbs
        article_item["bookmark"] = bookmark
        article_item["comments"] = comments
        article_item["contents"] = contents
        article_item["tags"] = tags
        article_item["author"] = author

        yield article_item
       '''
        # 通过itemloader加载item
        front_image_url = response.meta.get("front_image_url", "")
        item_loader = ArticleItemLoader(item=JobBoleArticleItem(), response=response)
        # item_loader.add_css(),item_loader.add_value(),item_loader_add_xpath()
        # item_loader会自动做.extract()方法
        item_loader.add_css("title", ".entry-header h1::text")
        item_loader.add_css("createdate", ".entry-meta-hide-on-mobile::text")
        item_loader.add_value("url", response.url)
        item_loader.add_value("url_object_id", common.get_md5(response.url))
        item_loader.add_value("front_image_url", [front_image_url])
        item_loader.add_css("thumbs", "span[class*='vote-post-up'] h10::text")
        item_loader.add_css("bookmark", "span[class*='bookmark-btn']::text")
        item_loader.add_css("comments", "div.post-adds a span::text")
        item_loader.add_css("contents", "div.entry")
        item_loader.add_css("tags", "p.entry-meta-hide-on-mobile a::text")
        item_loader.add_css("author", ".copyright-area > a::text")

        article_item = item_loader.load_item()

        yield article_item
