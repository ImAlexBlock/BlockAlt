import re
from datetime import datetime
import time
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import random
import string

app = FastAPI()  # docs_url=None

print('''+==================================================================================+
|   _____                   ____               _     _           _     ____  ___   |
|  |  ___|_ __  ___   ___  / ___| ___    ___  | | __(_)  ___    / \   |  _ \|_ _|  |
|  | |_  | '__|/ _ \ / _ \| |    / _ \  / _ \ | |/ /| | / _ \  / _ \  | |_) || |   |
|  |  _| | |  |  __/|  __/| |___| (_) || (_) ||   < | ||  __/ / ___ \ |  __/ | |   |
|  |_|   |_|   \___| \___| \____|\___/  \___/ |_|\_\|_| \___|/_/   \_\|_|   |___|  |
+==================================================================================+''')
print('Powered by AlexBlock\nRelease: 2024-05-27\nVersion: 1.4.0')

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


def random_cookie():
    cookie_template = {
        "sauth_json": "{\"gameid\": \"x19\", \"app_channel\": \"4399pc\", \"login_channel\": \"4399pc\", \"platform\": \"pc\", \"sdkuid\": \"267384159\", \"sessionid\": \"$sessionid\", \"udid\": \"$udid\", \"deviceid\": \"$deviceid\", \"aim_info\": \"{\\\"aim\\\":\\\"110.001.001.001\\\",\\\"country\\\":\\\"CN\\\",\\\"tz\\\":\\\"+0800\\\",\\\"tzid\\\":\\\"\\\"}\", \"client_login_sn\": \"$client_login_sn\", \"gas_token\": \"\", \"source_platform\": \"pc\", \"ip\": \"127.0.0.1\", \"userid\": \"$userid\", \"timestamp\": \"$timestamp\", \"realname\": \"{\\\"realname_type\\\":\\\"0\\\"}\", \"sdk_version\": \"1.0.0\"}"
    }
    values = {
        "sessionid": ''.join(random.choices(string.ascii_lowercase + string.digits, k=32)),
        "udid": ''.join(random.choices(string.ascii_uppercase + string.digits, k=10)),
        "deviceid": ''.join(random.choices(string.ascii_uppercase + string.digits, k=10)),
        "client_login_sn": ''.join(random.choices(string.ascii_uppercase + string.digits, k=32)),
        "userid": ''.join(random.choices(string.ascii_lowercase + string.digits, k=10)),
        "timestamp": str(random.randint(1000000000000, 9999999999999))
    }
    cookie = cookie_template["sauth_json"].replace("$sessionid", values["sessionid"]) \
        .replace("$udid", values["udid"]) \
        .replace("$deviceid", values["deviceid"]) \
        .replace("$client_login_sn", values["client_login_sn"]) \
        .replace("$userid", values["userid"]) \
        .replace("$timestamp", values["timestamp"])
    return cookie


def write_cookie(cookie):
    # 将cookie写入文件
    with open('cookie.txt', 'a') as file:
        file.write(cookie + '\n')


def check_ip_10min(ip):
    with open("get_count.csv") as file:
        lines = file.readlines()[-50:]  # 从后往前搜索最近的50行
        for line in reversed(lines):
            data = line.strip().split(',')
            if data[0] == ip:
                timestamp = datetime.strptime(data[1], '%Y-%m-%d %H:%M:%S')
                current_time = datetime.now()
                time_difference = (current_time - timestamp).total_seconds()
                if time_difference < 10:  # 这里是冷却时间
                    return True  # 查找到IP并且时间差小于10秒
                else:
                    return False  # 查找到IP但时间差大于等于10秒
        return False  # 未找到IP


def check_ip_last_10_get(ip):
    count = 0  # 计数器，用于记录匹配到的次数
    with open("get_count.csv") as file:
        lines = file.readlines()[-50:] if file else []  # 在文件为空的情况下将 lines 设为空列表
        if not lines:  # 若 lines 为空，则直接返回 True
            return True

        for line in reversed(lines):
            data = line.strip().split(',')
            if data[0] == ip:
                count += 1
                if count > 10:  # 匹配次数
                    return True
        return False


def check_ip(ip):
    if check_ip_10min(ip):
        if check_ip_last_10_get(ip):
            return False
        else:
            return True
    else:
        return True


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
        return "没货了，等待补货！"


# GetCookieAPI
@app.get("/free_cookie/get")
async def get_cookie(request: Request):
    if check_ip(request.client.host):
        cookie = cookie_get()
        with open('get_count.csv', 'a', encoding='utf-8') as file:
            file.write(request.client.host + ',' + get_time() + '\n')
        with open('log.txt', 'a', encoding='utf-8') as file:
            file.write('[' + get_time() + ']' + request.client.host + ':Get a cookie' + '\n')
        return {"status": 1, "cookie": cookie}
    else:
        with open('block_ip.csv', 'a', encoding='utf-8') as file:
            file.write(request.client.host + ',' + get_time() + '\n')
        with open('log.txt', 'a', encoding='utf-8') as file:
            file.write('[' + get_time() + ']' + request.client.host + ':Trigger frequency limit' + '\n')
        return {"status": 1, "cookie": random_cookie()}


# GetCookieCountAPI
@app.get("/free_cookie/count")
async def count(request: Request):
    with open('cookie.txt', 'r', encoding='utf-8') as file:
        lines = file.readlines()
    with open('log.txt', 'a', encoding='utf-8') as file:
        file.write('[' + get_time() + ']' + request.client.host + ':Check count' + '\n')
        return {"count": len(lines)}
