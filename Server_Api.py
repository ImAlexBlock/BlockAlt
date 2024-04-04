from typing import Union
from fastapi import FastAPI
import pymysql

app = FastAPI()

check_uid = 'SELECT MAX(uid) FROM user_data'
register = 'INSERT INTO user_data (uid, username, password, activation_code, get_count, status) VALUES (%s, %s, %s, %s, %s, %s)'
db_login = 'SELECT username, password FROM user_data WHERE username = %s AND password = %s'
db_info = 'SELECT (service_status, version, count_account, count_cookie, msg) FROM info'

try:
    conn = pymysql.connect(host='localhost', user='root', password='AlexBlock1337', db='blockalt')
    print('Connect to database!')
    cursor = conn.cursor()

except:
    print('Connection database failed!')


def check_activation_code(code_to_check):
    check_code = "SELECT code FROM activation_code WHERE code = %s"
    cursor.execute(check_code, (code_to_check,))  # 我们把你要查找的值赋给%s
    back_code = cursor.fetchone()

    if back_code is None:
        print("值未找到！")
        return False
    else:
        print("值已找到！")
        delete_code = "DELETE FROM activation_code WHERE code = %s"
        cursor.execute(delete_code, (code_to_check,))
        conn.commit()
        print("激活码已删除！")
        return True


@app.get("/blockalt/info")
def read_info():
    data = conn.cursor()
    sql = "SELECT service_status, version, count_account, count_cookie, msg FROM info"
    # 执行SQL语句
    data.execute(sql)
    # 获取一行查询结果
    info_data = data.fetchone()
    # 如果查询结果不为空，提取结果到不同的变量
    if info_data is not None:
        service_status, version, count_account, count_cookie, msg = info_data
        return {"service_status": service_status, "version": version, "count_account": count_account, "count_cookie": count_cookie, "msg": msg}


@app.get("/blockalt/register")
async def get_user(username: str, password: str, activation_code: str):
    print(username, password, activation_code)
    # 查询uid
    cursor.execute(check_uid)
    back_uid = cursor.fetchall()
    uid = back_uid[0][0] + 1

    # 查询激活码
    if check_activation_code(activation_code):
        print("激活码正确")
        status = 1
        cursor.execute(register, (uid, username, password, activation_code, '0', '1'))
        conn.commit()
        print('注册成功')

    else:
        status = 0
    return {"status": status}


@app.get("/blockalt/login")
async def get_user(username: str, password: str):
    cursor.execute("""
        SELECT username, password, status
        FROM user_data
        WHERE password = %s
        AND username = %s
    """, (password, username))
    back_user = cursor.fetchall()
    ban = back_user[0][2]
    print('status:', ban)
    if back_user and ban == 1:
        status = 1
        print("登录成功")
    elif ban == 2:
        status = 2
        print("账号已禁用")
    else:
        status = 0
    return {"status": status}


@app.get("/blockalt/get")
async def get_user(username: str, password: str):
    cursor.execute("""
        SELECT username, password, status
        FROM user_data
        WHERE password = %s
        AND username = %s
    """, (password, username))
    back_user = cursor.fetchall()
    ban = back_user[0][2]
    print('status:', ban)
    if back_user and ban == 1:
        status = 1
        print("登录成功")
    elif ban == 2:
        status = 2
        print("账号已禁用")
    else:
        status = 0
    return {"status": status}