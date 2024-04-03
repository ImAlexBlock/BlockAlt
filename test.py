import pymysql

# 打开数据库连接
try:
    conn = pymysql.connect(host='localhost', user='root', password='AlexBlock1337', db='blockalt')
    print('连接成功！')

    cursor = conn.cursor()

    sql = "SELECT service_status, version, count_account, count_cookie, msg FROM info"

    # 执行SQL语句
    cursor.execute(sql)

    # 获取一行查询结果
    row = cursor.fetchone()

    # 如果查询结果不为空，提取结果到不同的变量
    if row is not None:
        service_status, version, count_account, count_cookie, msg = row
        print(
            f"Service_status: {service_status}, Version: {version}, Count_account: {count_account}, Count_cookie: {count_cookie}, Msg: {msg}")

except Exception as e:
    print('连接失败：', e)



