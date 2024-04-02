import pymysql

# 打开数据库连接
try:
    conn = pymysql.connect(host='localhost', user='root', password='AlexBlock1337', db='blockalt')
    print('连接成功！')

    cursor = conn.cursor()

    sql = "INSERT INTO user_data(uid, username, password, activation_code, get_count, status) VALUES (%s, %s, %s, %s, %s, %s)"

    # 执行SQL语句
    cursor.execute(sql, ('1', 'Test', 'Test123', '114514', '0', '1'))

    # 提交到数据库
    conn.commit()
    conn.close()
except Exception as e:
    print('连接失败：', e)



