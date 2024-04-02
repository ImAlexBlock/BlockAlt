import string

import pymysql
import random

code_add = 'INSERT INTO activation_code(code) VALUES (%s)'


def random_string(numb):
    mix = string.ascii_letters + string.digits  # 混合字符包括大小写字母和数字
    return ''.join(random.choices(mix, k=numb))


try:
    conn = pymysql.connect(host='localhost', user='root', password='AlexBlock1337', db='blockalt')
    print('Connect to database!')
    cursor = conn.cursor()
    for i in range(int(input('生成激活码数量：'))):
        cursor.execute(code_add, (random_string(15)))
    conn.commit()
    cursor.close()
    print('Generate activation code successfully!')
except:
    print('Connection database failed!')
