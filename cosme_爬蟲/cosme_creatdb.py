import os
import pandas as pd
import sqlite3

# 建立資料庫連線
conn = sqlite3.connect('cosme.db')

def insert_data(conn, table_name, df):
    """ 將資料插入到指定的資料表 """
    try:
        # 清空表中的舊資料，避免資料重複
        conn.execute(f"DELETE FROM {table_name}")
        # 插入新的資料
        df.to_sql(table_name, conn, if_exists='append', index=False)
        print(f"資料成功插入到資料表 {table_name} 中")
    except Exception as e:
        print(f"插入資料到資料表 {table_name} 時發生錯誤：{e}")

# 資料夾路徑
folder_path = r'C:\Users\student\Desktop\cosme_project\cosme_csv'

# 列出資料夾中的所有檔案
for file_name in os.listdir(folder_path):
    if file_name.endswith('.csv'):
        table_name = file_name.split('.')[0]  # 使用 CSV 檔案名稱作為資料表名稱
        file_path = os.path.join(folder_path, file_name)
        df = pd.read_csv(file_path, encoding='utf-8', sep=',')

        # 建立資料表
        if file_name == 'cosme_goodbuy.csv':
            create_table_sql = f'''CREATE TABLE IF NOT EXISTS {table_name} (
                                     品牌名稱 VARCHAR,
                                     商品名稱 VARCHAR,
                                     cosme指數 REAL,
                                     人氣投票 INTEGER,
                                     銷售數量 INTEGER,
                                     評論數量 INTEGER,
                                     商品圖片 VARCHAR
                                     )'''
        else:
            create_table_sql = f'''CREATE TABLE IF NOT EXISTS {table_name} (
                                     排名 INTEGER,
                                     品牌名稱 VARCHAR,
                                     商品名稱 VARCHAR,
                                     價錢 INTEGER,
                                     評分 REAL,
                                     上市日期 VARCHAR,
                                     評論數量 INTEGER,
                                     商品圖片 VARCHAR
                                     )'''
        conn.execute(create_table_sql)
        insert_data(conn, table_name, df)

# 關閉連線
conn.close()
