#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""vultr.com connecting test"""

import sys
import re
import subprocess

v = """
Frankfurt, DE: https://fra-de-ping.vultr.com/vultr.com.100MB.bin
Paris, France: https://par-fr-ping.vultr.com/vultr.com.100MB.bin
Amsterdam, NL: https://ams-nl-ping.vultr.com/vultr.com.100MB.bin
London, UK: https://lon-gb-ping.vultr.com/vultr.com.100MB.bin
New York (NJ): https://nj-us-ping.vultr.com/vultr.com.100MB.bin
Singapore: https://sgp-ping.vultr.com/vultr.com.100MB.bin
Chicago, Illinois: https://il-us-ping.vultr.com/vultr.com.100MB.bin
Atlanta, Georgia: https://ga-us-ping.vultr.com/vultr.com.100MB.bin
Miami, Florida: https://fl-us-ping.vultr.com/vultr.com.100MB.bin
Tokyo, Japan: https://hnd-jp-ping.vultr.com/vultr.com.100MB.bin
Dallas, Texas: https://tx-us-ping.vultr.com/vultr.com.100MB.bin
Seattle, Washington: https://wa-us-ping.vultr.com/vultr.com.100MB.bin
Silicon Valley, California: https://sjo-ca-us-ping.vultr.com/vultr.com.100MB.bin
Los Angeles, California: https://lax-ca-us-ping.vultr.com/vultr.com.100MB.bin
Sydney, Australia: https://syd-au-ping.vultr.com/vultr.com.100MB.bin
"""

def ping_test(host, count=5):
    count =  str(count)
    if sys.platform.startswith('win'):
        def ping(host, count):
            import locale

            r = subprocess.run(['ping', '-n', count, host], stdout=subprocess.PIPE)
            if r.returncode == 0:
                out = r.stdout.decode(locale.getpreferredencoding()).strip()
                m = re.search(r'已发送 = ([0-9]+).*\(([0-9]+%) 丢失\).*平均 = ([0-9]+ms)', 
                              out, flags=re.DOTALL)
                if m:
                    return (m.group(1), m.group(2), m.group(3))
    else:
        def ping(host, count):
            import locale

            r = subprocess.run(['ping', '-c', count, host], stdout=subprocess.PIPE)
            if r.returncode == 0:
                out = r.stdout.decode(locale.getpreferredencoding()).strip()
                m = re.search(r'([0-9]+) packets transmitted,.*([0-9]+%) packet loss.*= ([^ ]+) ms', 
                              out, flags=re.DOTALL)
                if m:
                    min, avg, max, mdev = m.group(3).strip().split('/')
                    return (m.group(1), m.group(2), str(int(float(avg))) + ' ms')

    return ping(host, count)


def download_test(url):
    import locale
    from os import devnull
    r = subprocess.run(['wget', '--no-check-certificate', '-O', devnull, url], 
                       stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
    if r.returncode == 0:
        out = r.stdout.decode(locale.getpreferredencoding()).strip()
        m = re.search(r":[0-9]+ \(([0-9]+.*?)\).*`{}' saved".format(devnull), out)
        if m:
            return m.group(1)


def main():
    import argparse
    parser = argparse.ArgumentParser(description='vultr.com connecting test')
    args = parser.parse_args()

    for name, url in map(lambda x: x.split(': '), v.strip().split('\n')):
        host = url.split('/', 3)[2]
        r = ping_test(host)
        print(name, end=': ')
        if r:
            print('ping: {} packets transmitted, {} loss, {} agv'.format(*r), 
                  end='; ')
        r = download_test(url)
        if r:
            print('speed: {}'.format(r), end='')
        print()


if __name__ == '__main__':
    main()
