#!/usr/bin/env python3
# -*- coding: utf-8 -*-


def main():
    import sys

    lines = sys.stdin.read().strip().split('\n')
    sql_temp = lines.pop(0)[5:].strip()
    titles = lines.pop(0).strip().split('\t')
    d = {}
    for line in lines:
        lint = line.rstrip('\r')
        elements = line.split('\t')
        assert len(titles) == len(elements)
        d.clear()
        for i in range(len(titles)):
            d[titles[i]] = elements[i]
        print(sql_temp.format(**d) + ';')


if __name__ == '__main__':
    main()
