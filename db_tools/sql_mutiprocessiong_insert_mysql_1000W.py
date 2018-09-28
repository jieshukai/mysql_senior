#!/usr/bin/python
# -*- coding: UTF-8 -*-

# sql 用原生的  engine.execute 每次执行完自带commit 每次执行都会提交
#               session.execute 执行不会自带commit 可以最后一起提交，session.commit(),session.close()
#
import os
import time
from multiprocessing import Pool
from collections import deque
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from utils.random_data import random_nums, random_str

path = 'mysql+pymysql://root:root@localhost/mysql_senior?charset=utf8'
engine = create_engine(path, encoding='utf-8', echo=False)
engine.execute('SET autocommit=0;')
Session = sessionmaker(bind=engine)

def create_data(name, start, step):
    time_s = time.perf_counter()

    session = Session()
    # sql_str = "insert into emp(eid,ename,pid) values(%s,%s,%s);"
    sql_str = "insert into emp2(eid,ename,pid) values(:eid,:ename,:pid);"
    for i in range(step):
        session.execute(sql_str, {
            'eid': start + i,
            'ename': random_str(8),
            'pid': random_nums(3)
        })
    session.execute('commit;')
    session.commit()
    session.close()

    time_f = time.perf_counter()
    print('进程：{}，起始eid：{}，id：{}，耗时：{}'.format(name,start,os.getpid(),time_f-time_s))


def main(size, step):
    p = Pool(4)
    for i in range(size):
        start = queue.pop()
        # 进程无法传递 数据库连接等
        p.apply_async(create_data, args=(i, start, step))
    print('Waiting for all subprocesses done...')
    p.close()  # 先关闭进程池，不再添加新的进程
    p.join()  # wait 阻塞进程 直到所有任务结束
    print('All subprocesses done.')


if __name__ == '__main__':
    # 队列
    # Base.metadata.create_all(engine)
    print('Parent process %s.' % os.getpid())
    exp_time = time.perf_counter()

    exp = 6  # 2^22=400W 10^7=1000W
    start = 10**(exp-1)
    total = 10**exp
    step = 10000

    exp_time_stop = time.perf_counter()
    print('指数计算时间',exp_time_stop-exp_time)
    queue = deque()
    [queue.appendleft(i) for i in range(start, total, step)]
    size = len(queue)

    # 执行主任务
    time_start_session = time.perf_counter()

    main(size, step)
    time_s = time.perf_counter()

    time_stop_session = time.perf_counter()
    print('生成总数量==', total)
    print('总耗时====', -time_start_session + time_stop_session)
    print('步长-------', step)
    print('进程数量-------', size)
