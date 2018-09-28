# 计算  多进程
# io 多线程

import time
from queue import Queue
from threading import Thread

from faker import Factory
from sqlalchemy import create_engine, Column, VARCHAR
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from utils.random_data import random_nums

path = 'mysql+pymysql://root:root@localhost/mysql_senior?charset=utf8'
engine = create_engine(path, encoding='utf-8', echo=False)
Session = sessionmaker(bind=engine)
session = Session()

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


def create_data(start, step):
    faker_emps = [Emp(
        eid=i + start,
        ename=faker.name(),
        esalary=random_nums(4),
        pid=int(random_nums(3))
    ) for i in range(step)]
    session.add_all(faker_emps)


def thread_add_data(name, step):
    while not q.empty():
        start = q.get()
        print('线程{} 开始值{}'.format(name, start))
        create_data(start, step)
        print('开始值--', start, '--创建数据成功')
        q.task_done()


def main(size, step):
    ts = []
    for name in range(size):
        t = Thread(target=thread_add_data, args=(name, step))
        t.start()
        ts.append(t)

    q.join()


if __name__ == '__main__':
    # 队列
    # Base.metadata.create_all(engine)

    start = 10 ** 4
    total = 5 * 10 ** 4 + start
    step = total >> 5
    q = Queue()
    [q.put(i) for i in range(start, total, step)]  # 任务生成
    size = q.qsize()

    # 执行主任务
    time_start_session = time.perf_counter()
    main(size, step)
    time_stop_add = time.perf_counter()
    # 数据全部创建完成后再进行提交

    session.commit()
    session.close() # 一定要将session 关闭 否则接下来容易连接不到数据库
    time_stop_session = time.perf_counter()

    print('总耗时====', time_start_session - time_stop_session)
    print('生成数据耗时',time_start_session - time_stop_add)
    print('提交数据耗时',time_stop_add - time_stop_session)
    print('步长-------', step)
    print('进程数量-------', size)
