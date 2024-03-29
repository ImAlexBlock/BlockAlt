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


# 主窗口
root = tk.Tk()
root.geometry("300x240")
root.title("GetAlt 1.0")
root.resizable(False, False)

account_var = tk.StringVar()
password_var = tk.StringVar()


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
label_account = ttk.Label(root, text="Account")
entry_account = ttk.Entry(root, textvariable=account_var)
label_password = ttk.Label(root, text="Password")
entry_password = ttk.Entry(root, textvariable=password_var)
btn_copy_account = ttk.Button(root, text="Copy", command=lambda: copy_to_clipboard(account_var.get()))
btn_copy_password = ttk.Button(root, text="Copy", command=lambda: copy_to_clipboard(password_var.get()))
btn_module = ttk.Button(root, text="Account", command=on_change)
btn_get = ttk.Button(root, text="Get", command=on_get)
btn_info = ttk.Button(root, text="Info", command=on_info)

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

root.mainloop()