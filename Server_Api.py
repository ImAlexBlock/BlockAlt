from typing import Union
from fastapi import FastAPI

app = FastAPI()


@app.get("/blockalt/status")
def read_root():
    return {"status": 1, "version": "240330"} # statusID = 1 正常 2 维护


@app.get("/blockalt/info")
def read_info():
    return {"account": 10, "cookie": 20}


@app.get("/blockalt/register")
async def get_user(username: str, password: str, activation_code: str):
    print(username, password, activation_code)
    return {"status": 1, "msg": "注册成功"}