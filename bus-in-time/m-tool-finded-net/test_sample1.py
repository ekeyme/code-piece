#!/home/mozz/opt/bin/python3
# -*- coding: utf-8 -*-
import httplib2
from pprint import pprint
import time
import json
import random
import os
from os.path import dirname, abspath
from pyquery import PyQuery


#httplib2.debuglevel = 1
FIREFOX_AGENT = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; rv:45.0) Gecko/20100101 Firefox/45.0',
    'Accept-Language':'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
    'Accept-Encoding':'gzip, deflate',
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Connection':'keep-alive'}
STATIONS = ('科学城（天泰二路）总站', '天丰路站', '揽月路站', '广州科技创新基地站', '科丰路北站', 
    '科丰路中站', '上堂站', '姬堂站', '丰乐北横路口站', '碧山村站', '黄埔体育馆站', '丰乐北路站', 
    '大沙东站', '大沙西站', '大沙地站', '黄埔港总站')


def station_parse(content):
    '''Parsing bus station and check station.
    '''
    OFF = '0-0'
    stations = []
    bus_status = []
    content = json.loads(content[3:].decode('utf-8'))
    status = content['status']
    info = content['info']
    if status == 1 and info != '':
        pqContent = PyQuery(info)('#upInfo li')
        for station in pqContent:
            pqStation = PyQuery(station)
            station_name = pqStation('.station').text()
            stations.append(station_name)
            buses = pqStation.find('.bus')
            if buses.size() > 0:
                left_count = 0
                on_station_count = 0
                for bus in buses:
                    if PyQuery(bus).attr('style'):
                        left_count+=1
                    else:
                        on_station_count+=1
                bus_status.append('{0}-{1}'.format(on_station_count, left_count))
            else:
                bus_status.append(OFF)
    if not stations:
        return None

    return (tuple(bus_status), tuple(stations))

def main():
    '''main
    '''
    h = httplib2.Http('./tmp/cache', timeout=180)

    # initial to get cookie
    i = 1
    while i < 3:
        i+=1
        r, c = h.request('http://m.tool.finded.net/index.php?m=Bus&c=Bus&a=line&l=Ysaa4uFcm75skQuLm0TI1w-2x-2x%2F0', 
                headers=FIREFOX_AGENT)
        if r.status == 200:  break
        time.sleep(random.randint(2, 6))
    assert r.status == 200, 'initial connecting fail.'
    headers = FIREFOX_AGENT.copy()
    headers.update({'Cookie':r['set-cookie']})
    headers.update({'Accept':'application/json, text/javascript, */*; q=0.01'})
    headers.update({'X-Requested-With':'XMLHttpRequest'})
    headers.update({'Referer':'http://m.tool.finded.net/index.php?m=Bus&c=Bus&a=line&l=Ysaa4uFcm75skQuLm0TI1w-2x-2x%2F0'})
    
    # waiting do as like human
    time.sleep(random.randint(5, 15))
    connecting_fail_time = 0
    no_result_time = 0
    import sqlite3
    conn = sqlite3.connect('./database/m-tool-finded-net.sqlite3')
    cur = conn.cursor()
    while True:
        request_start_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        r, c = h.request('http://m.tool.finded.net/index.php?m=Bus&c=Bus&a=refresh&l=Ysaa4uFcm75skQuLm0TI1w-2x-2x/1', 
                headers=headers)
        request_end_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        if r.status == 200:
            connecting_fail_time = 0
            result = station_parse(c)
            if result:
                no_result_time = 0
                bus_status, stations = result
                assert stations == STATIONS, 'station changed: {0}'.format(str(stations))
                v = list(bus_status)
                v.insert(0, request_end_time)
                v.insert(0, request_start_time)
                cur.execute('''INSERT INTO Re326 (request_start_time, request_end_time, station1, station2, station3, station4, station5, station6, station7, station8, station9, station10, station11, station12, station13, station14, station15, station16) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', v)
                conn.commit()
            else:
                no_result_time+=1
        else:
            connecting_fail_time+=1
        # if connectiong fail 3 times, exit
        assert connecting_fail_time < 4, 'get bus fail.'
        assert no_result_time < 11, 'continuing no result 11 times.'

        time.sleep(random.randint(20, 25))

if __name__ == '__main__':
    # working dir
    os.chdir(dirname(dirname(abspath(__file__))))
    with open('./tmp/Re326.pid', 'w') as f:
        f.write(str(os.getpid()))
    main()
