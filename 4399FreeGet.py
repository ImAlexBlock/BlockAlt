import time
from selenium import webdriver
from os import system
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import webbrowser

system("title 4399FreeGet")
while True:
    print("===========4399FreeGet==========")
    module = input("获取模式：\n1.账号密码\n2.Cookie\n(1 or 2):")
    numb = int(input("获取数量："))
    options = Options()
    options.headless = True
    driver = webdriver.Chrome(options=options)
    driver.set_window_size(800, 800)
    driver.implicitly_wait(20)
    driver.get("https://4399.js.mcdds.cn/")
    count = 0

    try:
        element = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//h3[contains(text(),'免费4399小号获取')]"))
        )
        print("人机验证通过，开始获取小号")
        if module == "1":
            for i in range(numb):
                element = driver.find_element(By.XPATH, "//p[@id='get']")
                element.click()
                time.sleep(3)
                account = driver.find_element(By.XPATH, "//p[@id='account']")
                password = driver.find_element(By.XPATH, "//p[@id='password']")
                data = account.text + ":" + password.text
                print("获取到账号：" + data)
                with open('account.txt', 'a') as f:
                    f.write(data + '\n')
                for i in range(10, 0, -1):
                    print(f'\r冷却中！还有{i}秒', end='', flush=True)
                    time.sleep(1)
                print("\r ")
                print('\n')

        elif module == "2":
            for i in range(numb):
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                element = driver.find_element(By.XPATH, "//p[@id='get2']")
                element.click()
                time.sleep(3)
                data = driver.find_element(By.XPATH, "//p[@id='account2']")
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                print("获取到Cookie：" + data.text)
                with open('cookie.txt', 'a') as f:
                    f.write(data.text + "'\n'")
                for i in range(10, 0, -1):
                    print(f'\r冷却中！还有{i}秒', end='', flush=True)
                    time.sleep(1)
                print('\n')
        else:
            print("选的什么B模式，得帕金森了？还是打算去看脑科？")
    except:
        print("人机验证失败，请手动通过")
        print("帮你打开浏览器了，快去解锁吧！")
        webbrowser.open('https://4399.js.mcdds.cn/')