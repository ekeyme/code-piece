#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2017-06-21 20:22:39
# Project: test

import re
from urllib.parse import unquote
from pyspider.libs.base_handler import *


class Handler(BaseHandler):
    crawl_config = {
    }

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl('https://s.2.taobao.com/list/list.htm?spm=2007.1000337.0.0.fHqE43&st_trust=1&q=iphone+6s+%D2%F8&ist=0', callback=self.index_page)

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        for item in response.doc("#J_ItemListsContainer .item-lists li").items():
            # item info
            item_doc = item('.item-info')
            _d = item_doc('.item-title a')
            title = _d.text()
            url = _d.attr('href')
            r = re.search('[^\w]id=(\d+)', url)
            if not r:
                continue
            id = r.group(1)
            price = item_doc('.item-price .price em').text()
            desc = item_doc('.item-description').text()
            pub_time = item_doc('.item-pub-info .item-pub-time').text()
            comment_num = item_doc('.item-comments .number').text()

            # seller
            seller_doc = item('.seller-info-wrapper')
            seller_items_url = seller_doc('div[class="seller-nick"] a').attr('href')
            nickname = unquote(re.search('[^\w]usernick=([^&]+)', seller_items_url).group(1), response.encoding)
            
        # next page
        next_page = response.doc('#J_Pages a[class*="paginator-next"]').attr('href')
        if next_page:
            self.crawl('https:'+next_page, callback=self.index_page)

    @config(priority=2)
    def detail_page(self, response):
        return {
            "url": response.url,
            "title": response.doc('title').text(),
        }
