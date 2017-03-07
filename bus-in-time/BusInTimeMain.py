# -*- coding: utf-8 -*-
#!/usr/bin/env python3

    1. # -*- coding: utf-8 -*-
    2. import multiprocessing as mp
    3. import os
    4. import random
    5. from signal import signal, SIGINT, SIG_IGN, siginterrupt
    6. import time
    7. 
    8. def data_source():
    9.     """数据源。
    10. 
    11.     随机选择一个浮点数，作为worker进程的sleep时间，
    12.     具体实践时可以将这部分实现改为读取数据库。
    13.     """
    14.     dataset = [0.1, 0.2, 0.3, 0.4, 0.5]
    15.     while True:
    16.         time.sleep(0.2)
    17.         yield random.choice(dataset)
    18. 
    19. def proc_proxy(cntl_q, data_q, exit_flag):
    20.     """从数据源读取数据。
    21. 
    22.     先通过cntl_q通知主进程，
    23.     再将数据通过data_q发给worker。
    24.     """
    25.     for item in data_source():
    26.         cntl_q.put({'event': 'data'})
    27.         data_q.put(item)
    28.         if exit_flag.is_set():
    29.             cntl_q.put({'event': 'exit', 'pid': os.getpid()})
    30.             break
    31. 
    32. 
    33. def proc_worker(cntl_q, data_q):
    34.     """处理数据。
    35. 
    36.     从data_q获取数据，处理完毕后通过cntl_q通知主进程，
    37.     然后退出。
    38.     """
    39.     item = data_q.get()
    40.     time.sleep(item)
    41.     cntl_q.put({'event': 'exit', 'pid': os.getpid()})
    42. 
    43. def main():
    44.     proc_pool = {} # 记录创建的所有子进程
    45.     cntl_q = mp.Queue() # 控制信息传递队列
    46.     data_q = mp.Queue() # 具体数据传递队列
    47.     exit_flag = mp.Event() # 退出标记，初始值为False
    48. 
    49.     # 收到SIGINT，通知proxy停止读取数据
    50.     signal(SIGINT, lambda x, y: exit_flag.set())
    51.     siginterrupt(SIGINT, False)
    52. 
    53.     # 启动proxy进程，后续按需启动woker进程
    54.     print 'main {} started'.format(os.getpid())
    55.     proc = mp.Process(target=proc_proxy, args=(cntl_q, data_q, exit_flag))
    56.     proc.start()
    57.     proc_pool[proc.pid] = proc
    58.     print 'proxy {} started'.format(proc.pid)
    59. 
    60.     while True:
    61.         item = cntl_q.get()
    62.         if item['event'] == 'data':
    63.             proc = mp.Process(target=proc_worker, args=(cntl_q, data_q))
    64.             proc.start()
    65.             proc_pool[proc.pid] = proc
    66.             print 'worker {} started'.format(proc.pid)
    67.         elif item['event'] == 'exit':
    68.             proc = proc_pool.pop(item['pid'])
    69.             proc.join()
    70.             print 'child {} stopped'.format(item['pid'])
    71.         else:
    72.             print 'It\'s impossible !'
    73. 
    74.         if not proc_pool: # 所有子进程均已退出
    75.             break
    76. 
    77.     print 'main {} stopped'.format(os.getpid())
    78. 
    79. if __name__ == '__main__':
    80.     main()

