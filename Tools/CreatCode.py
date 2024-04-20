import string

import pymysql
import random

code_add = 'INSERT INTO activation_code(code) VALUES (%s)'


def random_string(numb):
    mix = string.ascii_letters + string.digits  # 混合字符包括大小写字母和数字
    return ''.join(random.choices(mix, k=numb))


try:
    conn = pymysql.connect(host='154.40.44.143', user='blockalt', password='yx5x6s2JY742tX47', db='blockalt')
    print('Connect to database!')
    cursor = conn.cursor()
    for i in range(int(input('生成激活码数量：'))):
        code = 'BlockAlt_' + random_string(15)
        cursor.execute(code_add, (code,))
        print(f'Generated: {code}')
        with open('code.txt', 'a') as file:
            file.write(code + '\n')
    conn.commit()
    cursor.close()
    print('Generate activation code successfully!')
except:
    print('Connection database failed!')
