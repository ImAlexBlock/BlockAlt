import re
from datetime import datetime
import time
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

print("FreeCookieAPI by AlexBlock")
print("Build240508")

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"]
)


def get_time():
    # 获取当前时间并格式化
    time_is = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    return time_is


def check_ip(ip, cd):
    with open("get_count.csv") as file:
        lines = file.readlines()[-50:]  # 从后往前搜索最近的50行
        for line in reversed(lines):
            data = line.strip().split(',')
            if data[0] == ip:
                timestamp = datetime.strptime(data[1], '%Y-%m-%d %H:%M:%S')
                current_time = datetime.now()
                time_difference = (current_time - timestamp).total_seconds()
                if time_difference < cd:
                    return False  # 如果查找到IP并且时间差小于10秒，则返回False
                else:
                    return True  # 如果查找到IP但时间差大于等于10秒，则返回True
        return True  # 如果未找到IP，则返回True


def process_cookie_line(line):
    match = re.search(r'{.*}', line)
    if match:
        return match.group(0)
    else:
        return None


def cookie_get():
    with open('cookie.txt', 'r+') as file:
        lines = file.readlines()
        for i, line in enumerate(lines):
            cookie = process_cookie_line(line)
            if cookie:
                del lines[i]
                file.seek(0)
                file.truncate()
                file.writelines(lines)
                return cookie
        return "没货了，快找AB补货"


# GetCookieAPI
@app.get("/free_cookie/get")
async def get_cookie(request: Request):
    if check_ip(request.client.host, 10):
        cookie = cookie_get()
        with open('get_count.csv', 'a', encoding='utf-8') as file:
            file.write(request.client.host + ',' + get_time() + '\n')
        return {"status": 1, "cookie": cookie}
    else:
        print('铸币[' + request.client.host + ']正在DDOS服务器!')
        with open('block_ip.csv', 'a', encoding='utf-8') as file:
            file.write(request.client.host + ',' + get_time() + '\n')
        return {"status": 0}


# GetCookieCountAPI
@app.get("/free_cookie/count")
async def count():
    with open('cookie.txt', 'r', encoding='utf-8') as file:
        lines = file.readlines()
        return {"count": len(lines)}
