from typing import Union
from fastapi import FastAPI
import pymysql

app = FastAPI()

check_uid = 'SELECT MAX(uid) FROM user_data'

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
        conn.commit()  # 别忘了提交事务哦
        print("激活码已删除！")
        return True


@app.get("/blockalt/status")
def read_root():
    return {"status": 1, "version": "240330"}  # statusID = 1 正常 2 维护


@app.get("/blockalt/info")
def read_info():
    return {"account": 10, "cookie": 20}


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

    return {"status": 1, "msg": "注册成功"}
