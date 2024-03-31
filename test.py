import pymysql

db = pymysql.connect(host='localhost', user='root', password='yourpassword', port=3306)
cursor = db.cursor()