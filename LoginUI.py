import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

def login():
    # 这里是登录按钮的回调函数
    # 可以添加验证用户名和密码的逻辑
    print("用户名:", entry_name.get())
    print("密码:", entry_password.get())
    # 这里只是一个示例弹窗
    messagebox.showinfo("登录信息", "登录成功！")

def register():
    # 这里是注册按钮的回调函数
    # 可以添加转到注册窗口的逻辑
    messagebox.showinfo("注册窗口", "跳转到注册窗口！")

# 创建主窗口
login_ui = tk.Tk()
login_ui.title("登录窗口")

# 设置窗口大小和位置
login_ui.geometry("270x135")

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