# create_db.py
import mysql.connector
from db_config import DB_CONFIG

conn = mysql.connector.connect(
    host=DB_CONFIG['host'],
    user=DB_CONFIG['user'],
    password=DB_CONFIG['password']
)

cursor = conn.cursor()

cursor.execute("CREATE DATABASE IF NOT EXISTS pension_management;")

print("数据库创建成功！")

cursor.close()
conn.close()
