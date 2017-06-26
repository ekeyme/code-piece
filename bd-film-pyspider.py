#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2017-06-25 21:46:49
# Project: bd_film

from pyspider.libs.base_handler import *
import re


class Handler(BaseHandler):
    crawl_config = {
        'itag': 'v1'
    }

    @every(minutes=24 * 60)
    def on_start(self):
        urls = ['http://www.bd-film.com/zx/',
                'http://www.bd-film.com/gq/',
                'http://www.bd-film.com/jd/',
                'http://www.bd-film.com/dh/']
        for url in urls:
            self.crawl(url+'index.htm', callback=self.detect_page, save={'url': url})

    @config(age=24 * 60 * 60)
    def detect_page(self, response):
        last_page = response.doc('.pagination > ul:nth-child(1) > li:nth-child(11) > a:nth-child(1)').attr('href')
        last_page_num = int(re.search(r'index_(\d+)\.htm', last_page).group(1))
        for p in range(1, last_page_num+1):
            self.crawl('{}index_{}.htm'.format(response.save['url'], p), callback=self.index_page)

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        for each in response.doc('table.table:nth-child(1) tr td a[href^="http://www.bd-film.com"]:nth-child(3)').items():
            self.crawl(each.attr.href, callback=self.detail_page, fetch_type='js')

    @config(priority=2)
    def detail_page(self, response):
        douban = response.doc('.list-douban').text()
        imdb = response.doc('.list-imdb').text()
        thunder = list(self.get_thunder_urls(response.doc))
        return {
            "update_time": re.search(r'最后更新时间： *(\d{4}-\d{2}-\d{2}) ', response.doc('#content > div:nth-child(2) > div:nth-child(2) > h6:nth-child(1)').text()).group(1),
            "douban": float(douban) if douban else 0,
            "imdb": float(imdb) if imdb else 0,
            "url": response.url,
            "thunder": thunder,
            "title": response.doc('#content > div:nth-child(2) > h3:nth-child(1)').text(),
        }

    def get_thunder_urls(self, doc):
        for each in doc('#bs-docs-download table tr').items():
            thunder = each('td a[href^="thunder://"]')
            if thunder:
                yield (each('.bd-address a').text(), thunder.attr.href)
