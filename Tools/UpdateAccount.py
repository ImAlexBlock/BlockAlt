import re
import pymysql

def get_and_remove_first_line(filepath, process_line_func=lambda x: x):
    with open(filepath, 'r') as file:
        lines = file.readlines()
    if not lines:
        return None
    first_line = process_line_func(lines[0].strip())
    update_file_content(filepath, lines[1:])
    return first_line


def update_file_content(filepath, remaining_lines):
    with open(filepath, 'w') as file:
        file.writelines(remaining_lines)


def get_account():
    def process_account_line(line):
        username, password = line.split(':')
        return username.strip('"'), password.strip('"')

    return get_and_remove_first_line('account.txt', process_account_line)


def get_cookie():
    def process_cookie_line(line):
        match = re.search(r'{.*}', line)
        if match:
            return match.group(0)
        else:
            return None

    return get_and_remove_first_line('cookie.txt', process_cookie_line)



try:
    conn = pymysql.connect(host='localhost', user='root', password='AlexBlock1337', db='blockalt')
    print('Connected!')
    module = input('输入添加类型（1.account;2.cookie）：')
    tick = int(input("输入添加数量："))
    cursor = conn.cursor()
    if module == '1':
        for i in range(tick):
            username, password = get_account()
            sql = "INSERT INTO account(name, password) VALUES (%s, %s)"
            # 使用占位符执行SQL语句
            cursor.execute(sql, (username, password))
            # 提交到数据库执行
            conn.commit()
            print(username + ':' + password)
    elif module == '2':
        for i in range(tick):
            cookie = get_cookie()
            sql = "INSERT INTO cookie (cookie) VALUES (%s)"
            cursor.execute(sql, (cookie,))
            conn.commit()
            print(cookie)
    conn.close()
except:
    print('Error!')

