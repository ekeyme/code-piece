# encoding: utf-8
"""
一个遍历内嵌列表(list)的模块""""""这是"nester.py"模块，
提供了一个名为print_lol()的函数，这个函数的作用是打印列表，
可以将列表内容打印至文件或者标准输出其中有可能包含（也有可能不包含）
嵌套列表

"""

import sys

def print_lol(a_list, indent=False, level=0, file_name=sys.stdout):
    """遍历list，包括内嵌list"""

    for each_item in a_list:
        if isinstance(each_item, list):
            print_lol(each_item, indent, level+1, file_name)
        else:
            if indent:
                for tab_stop in range(level):
                    print("\t", end='', file=file_name)
            
            print(each_item, file=file_name)
