import mysql.connector
import pandas as pd
import os
from db_config import DB_CONFIG
import pymysql
import math

# 连接到 MySQL 数据库
conn = pymysql.connect(
    host=DB_CONFIG['host'],
    user=DB_CONFIG['user'],
    password=DB_CONFIG['password'],
    database=DB_CONFIG['database']
)

cursor = conn.cursor()

# 定义一个函数来处理 NaN 和插入数据
def handle_nan(row):
    """将 NaN 替换为 None，以便 MySQL 插入 NULL 值"""
    return [None if isinstance(value, float) and math.isnan(value) else value for value in row]

# 定义一个函数来导入CSV到MySQL表
def import_csv_to_mysql(csv_path, table_name):
    try:
        # 使用 pandas 读取 CSV 文件
        df = pd.read_csv(csv_path)
        
        # 替换 NaN 为 None（MySQL 识别为 NULL）
        df = df.where(pd.notnull(df), None)
        
        # 使用 pandas 的 to_sql 方法将数据导入 MySQL 表
        for i, row in df.iterrows():
            row = handle_nan(row)  # 处理 NaN
            sql = f"INSERT INTO {table_name} ({', '.join(df.columns)}) VALUES ({', '.join(['%s'] * len(row))})"
            cursor.execute(sql, tuple(row))
        
        # 提交更改
        conn.commit()
        print(f"Data from {csv_path} has been inserted into {table_name}.")
    except Exception as e:
        print(f"Error inserting data from {csv_path} into {table_name}: {e}")
        conn.rollback()

tables_and_files = {
    'Users': 'data/Users.csv',
    'UserRoles': 'data/UserRoles.csv',
    'GeneralUser': 'data/GeneralUser.csv',
    'SeniorUser': 'data/SeniorUser.csv',
    'SeniorHealthData': 'data/SeniorHealthData.csv',
    'FamilyCaregiver': 'data/FamilyCaregiver.csv',
    'FamilySeniorRelation': 'data/FamilySeniorRelation.csv',
    'Staff': 'data/Staff.csv',
    'Supervisor': 'data/Supervisor.csv',
    'ElderCareInstitution': 'data/ElderCareInstitution.csv',
    'FuneralInstitution': 'data/FuneralInstitution.csv',
    'StaffInstitution': 'data/StaffInstitution.csv',
    'FuneralInstitutionEvaluation': 'data/FuneralInstitutionEvaluation.csv',
    'ElderCareInstitutionEvaluation': 'data/ElderCareInstitutionEvaluation.csv',
    'EmergencyCall': 'data/EmergencyCall.csv',
    'EmergencyCallUser': 'data/EmergencyCallUser.csv',
    'Reservation': 'data/Reservation.csv',
    'Permissions': 'data/Permissions.csv',
    'RolePermissions': 'data/RolePermissions.csv'
    
    

    

}

# 遍历表名和CSV文件，将数据导入到MySQL
for table_name, csv_path in tables_and_files.items():
    if os.path.exists(csv_path):
        import_csv_to_mysql(csv_path, table_name)
    else:
        print(f"CSV file {csv_path} not found.")

# 关闭数据库连接
cursor.close()
conn.close()
