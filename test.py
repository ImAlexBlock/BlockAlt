import requests
from requests.exceptions import ConnectionError, Timeout, RequestException

api_status = "http://127.0.0.1:8000/blockalt/status"
api_info = "http://127.0.0.1:8000/blockalt/info"

try:
    print(requests.get(api_status).json())
except ConnectionError:
    print('连接到服务器失败！请检查你的网络连接或URL是否正确。')
except Timeout:
    print('请求超时！服务器可能太忙或网络延迟。请稍后重试。')
except RequestException as e:
    print(f'请求过程出现了问题: {e}')