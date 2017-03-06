#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import httplib2

http = httplib2.Http('/tmp', timeout=300)
FIREFOX_AGENT = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; rv:45.0) Gecko/20100101 Firefox/45.0',
    'Accept-Language':'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
    'Accept-Encoding':'gzip, deflate',
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Connection':'keep-alive'}


def request_url(url, headers={}):
    from sys import stderr
    from socket import timeout as Timeout

    _headers = FIREFOX_AGENT.copy()
    _headers.update(headers)
    try:
        r, c = http.request(url, headers=_headers)
    except OSError as e:
        print('OSError: {}: {}'.format(e, url), file=stderr)
        return None
    except Timeout as e:
        print('Timeout: {}: {}'.format(e, url), file=stderr)
        return None
    if r.status == 200:
        return (r, c)
    else:
        print('Invalid HTTP Status: {}: {}'.format(
                    r.status, url), file=stderr)


def get_amazon_price(url):
    from pyquery import PyQuery

    d = {}
    r = request_url(url)
    if not r:
        return None

    c = r[1].decode('utf8', errors='surrogateescape')
    pq = PyQuery(c)
    d['price'] = float(pq("#priceblock_ourprice").text()[1:])
    d['stock'] = 0
    stock_info = pq("#ddmAvailabilityMessage").text()
    if stock_info == '现在有货':
        d['stock'] = 1.0
    return d


def get_jd_price(url):
    import re
    import json

    d = {}
    r = request_url(url)
    if not r:
        return None
    c = r[1].decode('ascii', errors='surrogateescape')
    m = re.search(r'{.*}', c)
    if not m:
        print("Price json request fail: JD: "+c, file=sys.stderr)
        return None
    return json.loads(m.group(0))


def get_tmall_info_from_product_url(url):
    import time
    import datetime
    from datetime import timezone, timedelta
    from urllib.parse import parse_qs, urlparse

    d = {}
    q = parse_qs(urlparse(url)[-2])
    d['itemid'] = q["id"][0]

    if "cat_id" in q:
        d['cat_id'] = q["cat_id"][0]
    else:
        d['cat_id'] = 2
    d['timestamp'] = now_tstp = time.time()
    now_time = time.gmtime(now_tstp)
    date = datetime.date.fromtimestamp(now_tstp) - datetime.timedelta(days=2)
    d['cachedtimestamp'] = datetime.datetime(date.year, date.month, date.day, 
                                    hour=10, minute=11, second=11, 
                                    tzinfo=timezone(timedelta(0))).timestamp()
    return d


def construct_get_price_url(info):
    s = r"https://mdskip.taobao.com/core/initItemDetail.htm?isApparel=false&cartEnable=true&isForbidBuyItem=false&isPurchaseMallPage=false&offlineShop=false&isRegionLevel=true&queryMemberRight=true&isSecKill=false&addressLevel=4&tmallBuySupport=true&isUseInventoryCenter=true&cachedTimestamp={cachedtimestamp}&tryBeforeBuy=false&itemId={itemid}&showShopProm=false&sellerPreview=false&service3C=true&household=false&isAreaSell=true&callback=setMdskip&timestamp={timestamp}&isg=Au3tsMZYT2--ie1uNidBgU/u/Ydk/SET&isg2=AoSEczQYgMI2CTQOS_J6zdWrVAKDTqgH8o-Vzp4mp88dySCTxK_9l9wpf9jn&cat_id={cat_id}"
    return s.format(**info)


def get_tmall_priceinfo(product_url):
    import re
    import json

    info = get_tmall_info_from_product_url(product_url)
    url = construct_get_price_url(info)
    r = request_url(url, {"Referer": product_url})
    if not r:
        return

    m = re.search(r'{.*}', r[1].decode('utf8', errors='surrogateescape'))
    if not m:
        print("Price json request fail: Tmall: "+c, file=sys.stderr)
        return
    o = json.loads(m.group(0))
    if not o["isSuccess"]:
        print("Tmall json responsed but with fail status.", file=sys.stderr)
        return
    return o


def get_tmall_price(purl, skuid):
    from time import gmtime, strftime

    def filter_prom_list(prom_list, threshold_price):
        l = []
        for prom in prom_list:
            prom_price = float(prom["price"])
            if prom_price < threshold_price:
                start_time = strftime("%Y/%m/%d %H:%M", 
                                      gmtime(prom["startTime"]/1000))
                end_time = strftime("%Y/%m/%d %H:%M", 
                                    gmtime(prom["endTime"]/1000))

                l.append({"start_time": start_time, 
                          "end_time": end_time, 
                          "price": prom_price})
        return l

    price_info = get_tmall_priceinfo(purl)
    if not price_info:
        return
    d = {}
    defaul_info = price_info["defaultModel"]
    d["stock"] = defaul_info["inventoryDO"]["skuQuantity"][skuid]["quantity"]
    d["prom"] = defaul_info["itemPriceResultDO"]["hasDPromotion"]
    d["promMobile"] = defaul_info["itemPriceResultDO"]["hasMobileProm"]
    d["halfoff"] = defaul_info["itemPriceResultDO"]["halfOffItem"]

    item_pinfo = defaul_info["itemPriceResultDO"]["priceInfo"][skuid]
    d["price"] = float(item_pinfo["price"])
    if "promotionList" in item_pinfo:
        prom_price = float(sorted(item_pinfo["promotionList"], 
                                  key=lambda e: float(e["price"]))[0]["price"])
        if prom_price < d["price"]:
            d["price"] = prom_price

    d["suggestivePromotionList"] = []
    if "suggestivePromotionList" in item_pinfo:
        d["suggestivePromotionList"] = filter_prom_list(
                item_pinfo["suggestivePromotionList"], d["price"])
    return d


def get_now_strtime():
    import time
    t = time.localtime()
    return (time.strftime('%Y-%m-%d', t), time.strftime('%H:%M', t))


def main():
    f = open(sys.argv[1], 'a')

    url = r'https://www.amazon.cn/Kindle-Paperwhite%E7%94%B5%E5%AD%90%E4%B9%A6%E9%98%85%E8%AF%BB%E5%99%A8-300-ppi%E7%94%B5%E5%AD%90%E5%A2%A8%E6%B0%B4%E8%A7%A6%E6%8E%A7%E5%B1%8F-%E5%86%85%E7%BD%AE%E9%98%85%E8%AF%BB%E7%81%AF-%E8%B6%85%E9%95%BF%E7%BB%AD%E8%88%AA/dp/B00QJDOLIO/ref=fs_km?th=1'
    date, time = get_now_strtime()
    r = get_amazon_price(url)
    if r and r["stock"] > 0:
        price = str(r['price'])
        print("Kpw3 from amazon: " + price)
        print('\t'.join(('amazon', date, time, price)), file=f)

    url = r'https://p.3.cn/prices/mgets?callback=jQuery5667777&type=1&area=19_1601_3633_0&pdtk=&pduid=14877296939311922782532&pdpin=s1880441097511936&pdbp=0&skuIds=J_2002883'
    date, time = get_now_strtime()
    r = get_jd_price(url)
    if r:
        print("Kpw3 from JD: {}; m: {}; op: {}".format(
                r['p'], r['m'], r['op']))
        ext = "m: {}; op: {}".format(r['m'], r['op'])
        print('\t'.join(('JD', date, time, r['p'], ext)), file=f)

    # bug: httplib2 can not request this url
    url = r"https://detail.tmall.com/item.htm?spm=a220m.1000858.1000725.1.hLLmvq&id=522680881881&skuId=3111647558446&standard=1&user_id=2099020602&cat_id=2&is_b=1&rn=af7f86e64ce960819e9967ce06473df4"
    date, time = get_now_strtime()
    r = get_tmall_price(url, '3111647558446')
    if r and r['stock'] > 3:
        print("Kpw3 from Tmall: {price}; halfoff: {halfoff}; "
              "future promotion: {suggestivePromotionList}".format(**r))
        ext = "stock: {stock}; halfoff: {halfoff}; " \
              "future promotion: {suggestivePromotionList}".format(**r)
        print('\t'.join(('Tmall', date, time, str(r['price']), ext)), file=f)


if __name__ == '__main__':
    main()
