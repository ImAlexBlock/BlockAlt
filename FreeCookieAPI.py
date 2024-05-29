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
print('Powered by AlexBlock\nRelease: 2024-05-29\nVersion: 1.4.2')

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"]
)


def get_time():
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
    with open('cookie.txt', 'a') as file:
        file.write(cookie + '\n')


def check_ip_10s(ip):
    with open("get_count.csv") as file:
        lines = file.readlines()[-50:]
        for line in reversed(lines):
            data = line.strip().split(',')
            if data[0] == ip:
                timestamp = datetime.strptime(data[1], '%Y-%m-%d %H:%M:%S')
                current_time = datetime.now()
                time_difference = (current_time - timestamp).total_seconds()
                if time_difference < 10:  # 这里是冷却时间
                    return True
                else:
                    return False
        return False


def check_ip_last_get(ip):
    count = 0
    try:
        with open("get_count.csv", "r") as file:
            lines = file.readlines()[-100:]
            for line in reversed(lines):
                data = line.strip().split(',')
                if data[0] == ip:
                    count += 1
                    if count > 10:
                        return True
            return False
    except FileNotFoundError:
        print("文件未找到，请确保文件路径正确")
        return False


def check_ip(ip):
    if check_ip_10s(ip):
        with open('log.txt', 'a', encoding='utf-8') as file:
            file.write('[' + get_time() + ']' + ip + ':Triggering the 10-second limit' + '\n')
        return False
    elif check_ip_last_get(ip):
        with open('log.txt', 'a', encoding='utf-8') as file:
            file.write('[' + get_time() + ']' + ip + ':The number of abnormal acquisitions detected' + '\n')
        with open('dog.txt', 'a', encoding='utf-8') as file:
            file.write('[' + get_time() + ']' + ip + '\n')
        return False
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
        return {"status": 1, "cookie": random_cookie()}


# GetCookieCountAPI
@app.get("/free_cookie/count")
async def count(request: Request):
    with open('cookie.txt', 'r', encoding='utf-8') as file:
        lines = file.readlines()
    with open('log.txt', 'a', encoding='utf-8') as file:
        file.write('[' + get_time() + ']' + request.client.host + ':Check count' + '\n')
        return {"count": len(lines)}
