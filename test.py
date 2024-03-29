import tkinter as tk
from tkinter import messagebox

def on_login():
    # 假设用户名和密码均为'admin'
    if username_entry.get() == 'admin' and password_entry.get() == 'admin':
        # 登录成功，关闭登录窗口
        login_window.destroy()
        # 打开主界面窗口
        open_main_window()
    else:
        messagebox.showerror('登录失败', '用户名或密码错误')

def open_main_window():
    main_window = tk.Toplevel()
    main_window.geometry('400x300')
    main_window.title('主界面')
    tk.Label(main_window, text='欢迎进入主界面！').pack()

# 创建登录窗口及其布局
login_window = tk.Tk()
login_window.geometry('200x150')
login_window.title('登录')

username_label = tk.Label(login_window, text='用户名：')
username_label.pack()

username_entry = tk.Entry(login_window)
username_entry.pack()

password_label = tk.Label(login_window, text='密码：')
password_label.pack()

password_entry = tk.Entry(login_window, show='*')
password_entry.pack()

login_button = tk.Button(login_window, text='登录', command=on_login)
login_button.pack()

login_window.mainloop()