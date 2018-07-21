# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.pipelines.images import ImagesPipeline
import codecs, json
from scrapy.exporters import JsonItemExporter
import MySQLdb
import MySQLdb.cursors
from twisted.enterprise import adbapi


class ArticlespiderPipeline(object):
    def process_item(self, item, spider):
        return item


class ArticleImagePipeline(ImagesPipeline):
    # 重写item_completed方法从results中获取到图片实际下载url路径
    def item_completed(self, results, item, info):
        # if isinstance(item, dict) or self.images_result_field in item.fields:
        #     item[self.images_result_field] = [x for ok, x in results if ok]
        # return item
        if "front_image_url" in item:
            for ok, value in results:
                image_file_path = value["path"]
            item["front_image_path"] = image_file_path

        return item


class JsonWithEncodingPipeline(object):
    # 自定义json文件的导出,保存到本地
    def __init__(self):
        # 使用codecs打開文件避免一些編碼問題
        self.file = codecs.open('article.json', 'w', encoding='utf8')

    def process_item(self, item, spider):
        # 将python数据通过json.dumps方法转换为json数据,json.dumps() &json.loads()
        # 处理文件用json,dump() & json.load()
        lines = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.file.write(lines)
        return item

    def spider_closed(self, spider):
        self.file.close()


class JsonExporterPipeline(object):
    # 调用scrapy提供的json exporter导出json文件
    def __init__(self):
        self.file = open('articlexport.json', 'wb')
        self.exporter = JsonItemExporter(self.file, encoding='utf-8', ensure_ascii=False)
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)  # 这一步完成了python数据到json的转换
        return item


class MysqlPipeline(object):
    # 采用同步的机制写入mysql
    def __init__(self):
        self.conn = MySQLdb.connect(host='127.0.0.1', user='root', password='123456',
                                    database='article_spider', charset="utf8", use_unicode=True)
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        insert_sql = """
            insert into article(title,createdate,url,url_object_id,
            front_image_url,front_image_path,thumbs,bookmark,comments,
            contents,tags,author)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """
        self.cursor.execute(insert_sql, (item["title"], item["createdate"],
                                         item["url"], item["url_object_id"],
                                         item["front_image_url"], item["front_image_path"], item["thumbs"],
                                         item["bookmark"], item["comments"], item["contents"], item["tags"],
                                         item["author"]))
        self.conn.commit()


class MysqlTwistedPipeline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool

    # @classmethod表示修饰的的from_settings方法是类专属的，并且可以通过类名访问
    @classmethod
    def from_settings(cls, settings):
        dbparms = dict(
            host=settings["MYSQL_HOST"],
            dbname=settings["MYSQL_DBNAME"],
            user=settings["MYSQL_USERT"],
            password=settings["MYSQL_PASSWORD"],
            charset='utf8',
            cursorclass=MySQLdb.cursors.DictCursor,
            use_unicode=True
        )
        dbpool = adbapi.ConnectionPool("MySQLdb", **dbparms)

        return cls(dbpool)

    def process_item(self, item, spider):
        # 使用twisted将mysql插入变成异步执行
        # 让写入数据库的操作实现异步
        query = self.dbpool.runInteraction(self.do_insert, item)
        # 处理异常
        query.addErrback(self.handle_error, item, spider)

    def handle_error(self, failure, item, spider):
        # 处理异步插入的异常
        print(failure)

    def do_insert(self, cursor, item):
        # insert_sql = """
        #     insert into article(title, url, createdate)
        #     VALUES (%s, %s, %s)
        # """
        # cursor.execute(insert_sql, (item["title"], item["url"], item["createdate"]))
        # 执行具体的插入
        # 根据不同的item 构建不同的sql语句并插入到mysql中
        insert_sql = """
            insert into article(title,createdate,url,url_object_id,
            front_image_url,front_image_path,thumbs,bookmark,comments,
            contents,tags,author)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """
        cursor.execute(insert_sql, (item["title"], item["createdate"],
                                         item["url"], item["url_object_id"],
                                         item["front_image_url"], item["front_image_path"], item["thumbs"],
                                         item["bookmark"], item["comments"], item["contents"], item["tags"],
                                         item["author"]))
        # insert_sql, params = item.get_insert_sql()
        # cursor.execute(insert_sql, params)
