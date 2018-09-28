import random
from string import ascii_letters, digits

import sys

if sys.version_info > (3, 5):
    def random_str(n):
        return ''.join(random.choices(ascii_letters, k=n))


    def random_nums(n):
        return ''.join(random.choices(digits, k=n))
else:
    # raise RuntimeError('At least Python 3.4 is required')
    # 由于 ubuntu python 版本3.5 没有choices,虽然很简单。。。
    def random_str(n):
        return ''.join([random.choice(ascii_letters) for i in range(n)])


    def random_nums(n):
        return ''.join([random.choices(digits) for i in range(n)])
