import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter.simpledialog import askstring
import pyperclip
import requests
import base64
from requests.exceptions import ConnectionError, Timeout, RequestException

get_module = 'Account'
version = '240403'
seconds = [10]  # 冷却时间

# api列表
api_status = "http://127.0.0.1:8000/blockalt/info"
api_info = "http://127.0.0.1:8000/blockalt/info"
api_register = "http://127.0.0.1:8000/blockalt/register"
api_login = "http://127.0.0.1:8000/blockalt/login"

# 验证服务器状态
try:
    get_status = requests.get(api_status).json()
    if get_status["service_status"] == 1:
        if get_status["version"] != version:
            messagebox.showerror("Check Version",
                                 f"检查版本更新！\n当前版本：{version}\n最新版本：{get_status['version']}")
            exit()
    if get_status["service_status"] == 2:
        messagebox.showerror("Error", "服务器维护中，请稍后再试！")
except RequestException:
    messagebox.showerror("Error",
                         f'''人生自古谁无死，遗憾的服务器已经死亡，无法继续与您互动。\n您可以检查网络后重试，如果问题持续发生请联系管理员！''')
    exit()


def update_file_content(filepath, remaining_lines):
    with open(filepath, 'w') as file:
        file.writelines(remaining_lines)


def get_and_remove_first_line(filepath, process_line_func=lambda x: x):
    with open(filepath, 'r') as file:
        lines = file.readlines()
    if not lines:
        return None
    first_line = process_line_func(lines[0].strip())
    update_file_content(filepath, lines[1:])
    return first_line


def get_account():
    def process_account_line(line):
        username, password = line.split(':')
        return username.strip('"'), password.strip('"')

    return get_and_remove_first_line('account.txt', process_account_line)


def get_cookie():
    def process_cookie_line(line):
        return line.strip().strip("'")

    return get_and_remove_first_line('cookie.txt', process_cookie_line)


def login():
    # print("Username:", entry_name.get())
    # print("Password:", entry_password.get())
    # 登录の逻辑
    username = entry_name.get()
    password = entry_password.get()
    try:
        response = requests.get(api_login + "?username=" + username + "&password=" + password).json()
        if response['status'] == 1:
            messagebox.showinfo("Login", "Successful!")
            # FastLogin
            login_data = entry_name.get() + ':' + entry_password.get()
            byte_data = base64.b64encode(login_data.encode('utf-8'))
            with open('fastlogin.txt', 'w') as file:
                file.write(byte_data.decode('utf-8'))
            # 关闭登录窗口，开启MainUI
            login_ui.destroy()
            main.deiconify()
            pass

        elif response['status'] == 2:
            messagebox.showerror("Login", f"人生自古谁无死？遗憾的 {username} 已经死亡。\n如果认为你比窦娥还冤，请寻找管理员！")
        else:
            messagebox.showerror("Login", "Failed!")
    except:
        messagebox.showerror("Login", "Please check your internet connection")



def register():
    username = entry_name.get()
    password = entry_password.get()
    code = askstring("Verify", "Activation Code:")
    try:
        request = requests.get(
            api_register + '?username=' + username + '&password=' + password + '&activation_code=' + code).json()
        if request['status'] == 1:
            messagebox.showinfo("Register", "Successful!\nThank you for choosing BlockAlt :-)")
        elif request['status'] == 0:
            messagebox.showerror("Register", "Please check your activation code status or ask admin for help")
            pass
    except:
        messagebox.showerror("Register", "Please check your internet connection")


# 主窗口
main = tk.Tk()
main.geometry("300x240")
main.title(f"BlockAlt {version}")
main.resizable(False, False)
main.withdraw()
account_var = tk.StringVar()
password_var = tk.StringVar()

login_ui = tk.Tk()
login_ui.title("Login & Register")
login_ui.geometry("270x135")
login_ui.resizable(False, False)


def copy_to_clipboard(text):
    pyperclip.copy(text)
    print("Copied to clipboard:", text)


def on_change():
    global get_module
    if get_module == "Account":
        get_module = "Cookie"
        btn_module.config(text=get_module)

    elif get_module == "Cookie":
        get_module = "Account"
        btn_module.config(text=get_module)


def cooldown(remaining=None):
    if remaining is not None:
        seconds[0] = remaining
    if seconds[0] > 0:
        btn_get['text'] = f'Cooldown:{seconds[0]}s'
        seconds[0] -= 1
        main.after(1000, cooldown)
    else:
        btn_get['text'] = 'Get'
        btn_get['state'] = 'normal'


def on_get():
    if get_module == "Account":
        username, password = get_account()
        if username and password:
            account_var.set(username)
            password_var.set(password)
        else:
            account_var.set("")
            password_var.set("")
            messagebox.showerror("Error", "No account found")

    elif get_module == "Cookie":
        cookie = get_cookie()
        if cookie:
            account_var.set(cookie)
            password_var.set("")
        else:
            messagebox.showerror("Error", "No cookie found")
            account_var.set("")
            password_var.set("")

    # 冷却时间
    btn_get['state'] = 'disabled'
    cooldown()


def on_info():
    try:
        get_status = requests.get(api_status).json()
        version = get_status['version']
        cookie = get_status['count_cookie']
        account = get_status['count_account']

    except:
        cookie = "Unknown"
        account = "Unknown"


    messagebox.showinfo("Info", f'''    BlockAlt © 2024 AlexBlock. All Rights Reserved.
    Version: {version}
    Website: https://alt.alexblock.org
    --------------------------------------------------------------
    Account: {account}
    Cookie: {cookie}
    ''')


def count_account():
    try:
        data = requests.get(api_info).json()
        count = data["account"]
        return count
    except RequestException:
        return 'N/A'


def count_cookie():
    try:
        data = requests.get(api_info).json()
        count = data["cookie"]
        return count
    except RequestException:
        return 'N/A'


# 界面元素
label_account = ttk.Label(main, text="Account")
entry_account = ttk.Entry(main, textvariable=account_var)
label_password = ttk.Label(main, text="Password")
entry_password = ttk.Entry(main, textvariable=password_var)
btn_copy_account = ttk.Button(main, text="Copy", command=lambda: copy_to_clipboard(account_var.get()))
btn_copy_password = ttk.Button(main, text="Copy", command=lambda: copy_to_clipboard(password_var.get()))
btn_module = ttk.Button(main, text="Account", command=on_change)
btn_get = ttk.Button(main, text="Get", command=on_get)
btn_info = ttk.Button(main, text="Info", command=on_info)

# 布局
label_account.grid(row=0, column=1, padx=10, pady=10)
entry_account.grid(row=1, column=1, padx=10, pady=10)
btn_copy_account.grid(row=1, column=4, padx=10, pady=10)
label_password.grid(row=2, column=1, padx=10, pady=10)
entry_password.grid(row=3, column=1, padx=10, pady=10)
btn_copy_password.grid(row=3, column=4, padx=10, pady=10)
btn_module.grid(row=4, column=4, padx=10, pady=10)
btn_get.grid(row=4, column=1, columnspan=3, sticky="ew", padx=10, pady=10)
btn_info.grid(row=0, column=4, padx=10, pady=10)

# Name
lbl_name = ttk.Label(login_ui, text="Name")
lbl_name.grid(row=0, column=0, padx=10, pady=10)
entry_name = ttk.Entry(login_ui)
entry_name.grid(row=0, column=1, columnspan=2, padx=10)

# Password
lbl_password = ttk.Label(login_ui, text="Password")
lbl_password.grid(row=1, column=0, padx=10, pady=10)
entry_password = ttk.Entry(login_ui, show="*")
entry_password.grid(row=1, column=1, columnspan=2, padx=10)

# 登录和注册按钮
btn_login = ttk.Button(login_ui, text="Login", command=login)
btn_login.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="ew")
btn_register = ttk.Button(login_ui, text="Register", command=register)
btn_register.grid(row=2, column=2, columnspan=2, padx=10, pady=10, sticky="ew")

# FastLogin
try:
    with open('fastlogin.txt', 'r') as file:
        encoded_string = file.read()

    # Base64解码
    decoded_bytes = base64.b64decode(encoded_string)
    decoded_string = decoded_bytes.decode('utf-8')
    data = decoded_string.split(':')
    entry_name.insert(0, data[0])
    entry_password.insert(0, data[1])

except:
    pass

# 循环
login_ui.mainloop()
main.mainloop()
