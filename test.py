import pymysql

# 打开数据库连接
try:
    conn = pymysql.connect(host='localhost', user='root', password='AlexBlock1337', db='blockalt')
    print('连接成功！')

    cursor = conn.cursor()

    cursor.execute("SELECT * FROM cookie LIMIT 1")
    result = cursor.fetchone()
    cookie = result[0]
    print(cookie)

except Exception as e:
    print('连接失败：', e)

# import re
#
#
# def get_and_remove_first_line(filepath, process_line_func=lambda x: x):
#     with open(filepath, 'r') as file:
#         lines = file.readlines()
#     if not lines:
#         return None
#     first_line = process_line_func(lines[0].strip())
#     update_file_content(filepath, lines[1:])
#     return first_line
#
#
# def update_file_content(filepath, remaining_lines):
#     with open(filepath, 'w') as file:
#         file.writelines(remaining_lines)
#
#
# def get_account():
#     def process_account_line(line):
#         username, password = line.split(':')
#         return username.strip('"'), password.strip('"')
#
#     return get_and_remove_first_line('account.txt', process_account_line)
#
#
# def get_cookie():
#     def process_cookie_line(line):
#         match = re.search(r'{.*}', line)
#         if match:
#             return match.group(0)
#         else:
#             return None
#
#     return get_and_remove_first_line('cookie.txt', process_cookie_line)
#
#
# username, password = get_account()
# print(f"Username: {username}, Password: {password}")
# print(get_cookie())