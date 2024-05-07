from fastapi import FastAPI, Request
import pymysql
import time

app = FastAPI()

try:
    conn = pymysql.connect(host='154.40.44.143', user='blockalt', password='yx5x6s2JY742tX47', db='blockalt')
    print('连接数据库成功!')
    cursor = conn.cursor()
except:
    print('连接数据库失败!')


def get_time():
    # 获取当前时间并格式化
    time_is = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    return time_is
# GetCookieAPI
cookie = ""
@app.get("/get_cookie")
async def get_cookie(request: Request):
    global cookie
    try:
        cursor.execute("SELECT * FROM cookie LIMIT 1")
        result = cursor.fetchone()
        cookie = result[0]
        print(request.client.host + ',' + get_time())
        with open('get_count.csv', 'a', encoding='utf-8') as file:
            file.write(request.client.host + ',' + get_time() + '\n')
        return {"status": 1, "cookie": cookie}
    except:
        return {"status": 0}
    finally:
        sql = "DELETE FROM cookie WHERE cookie = %s"
        cursor.execute(sql, (cookie,))
        conn.commit()
