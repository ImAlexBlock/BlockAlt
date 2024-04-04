import pymysql

# 打开数据库连接
try:
    conn = pymysql.connect(host='localhost', user='root', password='AlexBlock1337', db='blockalt')
    print('连接成功！')

    cursor = conn.cursor()

    sql = "SELECT service_status, version, count_account, count_cookie, msg FROM info"

    # 执行SQL语句
    cursor.execute(sql)

    # 获取一行查询结果
    row = cursor.fetchone()

    # 如果查询结果不为空，提取结果到不同的变量
    if row is not None:
        service_status, version, count_account, count_cookie, msg = row
        print(
            f"Service_status: {service_status}, Version: {version}, Count_account: {count_account}, Count_cookie: {count_cookie}, Msg: {msg}")

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
