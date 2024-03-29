import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import pyperclip

get_module = 'Account'

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
    # 这里是登录按钮的回调函数
    # 可以添加验证用户名和密码的逻辑
    print("Usernmae:", entry_name.get())
    print("Password:", entry_password.get())
    # 这里只是一个示例弹窗
    messagebox.showinfo("登录信息", "登录成功！")
    login_ui.destroy()
    main.deiconify()

def register():
    # 这里是注册按钮的回调函数
    # 可以添加转到注册窗口的逻辑
    messagebox.showinfo("注册窗口", "跳转到注册窗口！")


# 主窗口
main = tk.Tk()
main.geometry("300x240")
main.title("GetAlt 1.0")
main.resizable(False, False)
main.withdraw()
account_var = tk.StringVar()
password_var = tk.StringVar()

login_ui = tk.Tk()
login_ui.title("登录窗口")
login_ui.geometry("270x135")
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


def on_info():
    print("Info")
    messagebox.showinfo("Info", '''    GetAlt © 2018-2024 AlexBlock. All Rights Reserved.
    Version: 0.0.1  Build: 240330
    Website: https://alt.alexblock.org
    --------------------------------------------------------------
    Count:
    Account: 0
    Cookie: 0
    ''')


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

# 创建“Name”标签和输入框
lbl_name = ttk.Label(login_ui, text="Name")
lbl_name.grid(row=0, column=0, padx=10, pady=10)
entry_name = ttk.Entry(login_ui)
entry_name.grid(row=0, column=1, columnspan=2, padx=10)

# 创建“Password”标签和输入框
lbl_password = ttk.Label(login_ui, text="Password")
lbl_password.grid(row=1, column=0, padx=10, pady=10)
entry_password = ttk.Entry(login_ui, show="*")
entry_password.grid(row=1, column=1, columnspan=2, padx=10)

# 创建登录和注册按钮
btn_login = ttk.Button(login_ui, text="Login", command=login)
btn_login.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

btn_register = ttk.Button(login_ui, text="Register", command=register)
btn_register.grid(row=2, column=2, columnspan=2, padx=10, pady=10, sticky="ew")

# 启动主事件循环
login_ui.mainloop()
main.mainloop()