import pymysql

# 打开数据库连接
try:
    conn = pymysql.connect(host='localhost', user='root', password='AlexBlock1337', db='blockalt')
    print('连接成功！')
    cursor = conn.cursor()
    # # 插入数据
    # sql = "INSERT INTO user_data (uid, username, password, activation_code, get_count, status) VALUES (%s, %s, %s, %s, %s, %s)"
    # cursor.execute(sql, ('0', 'AlexBlock', '123456', 'fxZDNaDoubtKQKv', 0, 1))
    # # 提交，不然无法保存新建或者修改的数据
    # conn.commit()
    # # 关闭游标和连接
    # cursor.close()
    # conn.close()
    sql = "SELECT MAX(uid) FROM user_data"
    cursor.execute(sql)
    results = cursor.fetchall()
    print(results[0][0])
    uid = results[0][0] + 1
    print(uid)
    check_activation_code = "SELECT code FROM activation_code"
    cursor.execute(check_activation_code)
    back_activation_code = cursor.fetchall()
    print(back_activation_code)
    print('写入成功!')
except Exception as e:
    print('something wrong:', e)
