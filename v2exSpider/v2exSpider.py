#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2018-08-08 14:05:05
# Project: v2exSpider

from pyspider.libs.base_handler import *
import pymysql
import random


class Handler(BaseHandler):
    crawl_config = {
    }

    def __init__(self):
        self.db = pymysql.connect('localhost', 'root', 'ying1206', 'wenda', charset='utf8')

    def add_quesion(self, title, content):
        try:
            cur = self.db.cursor();
            sql = 'insert into  question (title,content,user_id,created_date,comment_count) values ("%s","%s",%d,now(),0)' % (
            title, content, random.randint(1, 20))
            print(sql)
            cur.execute(sql)
            self.db.commit()
        except Exception:
            print("Exception Here")
            self.db.rollback()
            raise Exception

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl('https://www.v2ex.com/go/qna?p=1', callback=self.index_page)

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        for each in response.doc('a[href^="https://www.v2ex.com/go/qna?p"]').items():
            self.crawl(each.attr.href, callback=self.list_page)

    @config(priority=2)
    def list_page(self, response):
        for each in response.doc('a[href^="https://www.v2ex.com/go/qna?p"]').items():
            self.crawl(each.attr.href, callback=self.list_page)
        for each in response.doc('a[href^="https://www.v2ex.com/t/"]').items():
            if each.attr.href.find("reply") > 0:
                self.crawl(each.attr.href, callback=self.question_page)

    @config(priority=2)
    def question_page(self, response):
        title = response.doc('div.header>h1').text()
        content = response.doc('div.markdown_body>p').text()
        self.add_quesion(title, content)
        return {
            "title": title,
            "content": content
        }
