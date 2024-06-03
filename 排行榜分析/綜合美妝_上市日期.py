import sqlite3
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# 連線資料庫
conn = sqlite3.connect(r"C:\Users\student\Desktop\cosme_project\cosme_py\cosme.db")
print("連線成功!")

# 查詢並轉換為 DataFrame
df_all = pd.read_sql('SELECT * FROM cosme_all', conn)

# 關閉連接
conn.close()

# 設定中文字體
plt.rcParams["font.family"] = "Microsoft JhengHei"
plt.rcParams["font.size"] = 20
plt.rcParams["axes.unicode_minus"] = False

# 使用Seaborn的調色板
colors = sns.color_palette('pastel')

# 將上市日期轉換為 datetime 格式
df_all['上市日期'] = pd.to_datetime(df_all['上市日期'], errors='coerce')

# 刪除包含 None 的行
df_all = df_all.dropna(subset=['上市日期'])

# 提取年度和季度作為新的欄位
df_all['年份'] = df_all['上市日期'].dt.year
df_all['季度'] = df_all['上市日期'].dt.quarter

# 計算每個季度的商品數量
quarterly_counts = df_all.groupby('季度').size().reset_index(name='商品數量')

# 繪製季度商品數量柱狀圖
plt.figure(figsize=(12, 8))
barplot_quarter = sns.barplot(data=quarterly_counts, x='季度', y='商品數量', palette='pastel', width=0.3)
plt.title('季度商品數量分佈情況', size="large", fontweight="bold")
plt.xlabel('季度')
plt.ylabel('商品數量')

# 添加資料標籤
for p in barplot_quarter.patches:
    barplot_quarter.annotate(format(p.get_height(), '.0f'), 
                             (p.get_x() + p.get_width() / 2., p.get_height()), 
                             ha = 'center', va = 'center', 
                             xytext = (0, 10), 
                             textcoords = 'offset points')

# 顯示圖表
plt.xticks(range(4), ['Q1', 'Q2', 'Q3', 'Q4'])  # 季度從1到4
plt.show()

# 繪製年度商品數量柱狀圖
yearly_counts = df_all.groupby('年份').size().reset_index(name='商品數量')
plt.figure(figsize=(12, 8))
barplot_year = sns.barplot(data=yearly_counts, x='年份', y='商品數量', palette='pastel', width=0.5)
plt.title('年度商品數量分佈情況', size="large", fontweight="bold")
plt.xlabel('年份')
plt.ylabel('商品數量')

# 將年份顯示為整數
barplot_year.xaxis.set_major_locator(ticker.MaxNLocator(integer=True))

# 添加資料標籤
for p in barplot_year.patches:
    barplot_year.annotate(format(p.get_height(), '.0f'), 
                          (p.get_x() + p.get_width() / 2., p.get_height()), 
                          ha = 'center', va = 'center', 
                          xytext = (0, 10), 
                          textcoords = 'offset points')

# 顯示圖表
plt.show()
