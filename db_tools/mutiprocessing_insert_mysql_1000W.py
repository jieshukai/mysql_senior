# 计算  多进程
# io 多线程
import os
import time
from multiprocessing import Pool
from collections import deque
from faker import Factory
from sqlalchemy import create_engine, Column, VARCHAR
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from utils.random_data import random_nums

path = 'mysql+pymysql://root:root@localhost/mysql_senior?charset=utf8'
engine = create_engine(path, encoding='utf-8', echo=False)
Session = sessionmaker(bind=engine)

# orm 对象
Base = declarative_base()


class Emp(Base):
    __tablename__ = 'emp'
    id = Column(INTEGER, primary_key=True, autoincrement=True, nullable=False)
    eid = Column(INTEGER)
    ename = Column(VARCHAR)
    esalary = Column(INTEGER)
    pid = Column(INTEGER)

    # author = relationship('User')
    def __str__(self):
        return self.ename


# 如果你玩过LOL, 我想你一定知道Faker。而在 Python的世界中，Faker 是用来生成虚假数据的库。
# pip install faker
faker = Factory.create()


def create_data(name, start, step):
    time_s = time.perf_counter()

    session = Session()
    print('Run child process %s (%s)...' % (name, os.getpid()))
    faker_emps = [Emp(
        eid=i + start,
        ename=faker.name(),
        esalary=random_nums(4),
        pid=int(random_nums(3))
    ) for i in range(step)]
    session.add_all(faker_emps)

    session.commit()
    session.close()
    print('end', start, 'start:  ', start)
    time_f = time.perf_counter()
    print(name, '-耗时--', time_f - time_s)


def main(size, step):
    p = Pool(size >> 2)
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

    start = 10 ** 6
    total = 5 * 10 ** 6 + start
    step = total >> 4
    queue = deque()
    [queue.appendleft(i) for i in range(start, total, step)]
    size = len(queue)

    # 执行主任务
    time_start_session = time.perf_counter()

    main(size, step)

    # 数据全部创建完成后再进行提交
    # 多进程 需要 在每个进程上单独提交
    # session.commit()
    # session.close()  # 一定要将session 关闭 否则接下来容易连接不到数据库
    time_stop_session = time.perf_counter()
    print('生成总数量==', total)
    print('总耗时====', -time_start_session + time_stop_session)
    print('步长-------', step)
    print('进程数量-------', size)
