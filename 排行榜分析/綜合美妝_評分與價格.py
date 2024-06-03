import sqlite3
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# 連線資料庫
conn = sqlite3.connect(r"C:\Users\student\Desktop\cosme_project\cosme_py\cosme.db")
print("連線成功!")

# 查詢並轉換為 DataFrame
df_all = pd.read_sql('SELECT * FROM cosme_all', conn)

# 關閉連接
conn.close()

# 設定中文(影響整個程式) "微軟正黑體Microsoft JhengHei"
plt.rcParams["font.family"] = "Microsoft JhengHei"
plt.rcParams["font.size"] = 20
plt.rcParams["axes.unicode_minus"] = False

# 使用Seaborn的調色板
colors = sns.color_palette('pastel')

# 1. 評分分析
plt.figure(figsize=(12, 8))
mean_rating = df_all["評分"].mean()
max_rating = df_all["評分"].max()
min_rating = df_all["評分"].min()

sns.histplot(df_all["評分"], bins=20, kde=True, color=colors[1])
plt.axvline(mean_rating, color='blue', linestyle='dashed', linewidth=2, label=f'平均: {mean_rating:.2f}')
plt.axvline(max_rating, color='green', linestyle='dashed', linewidth=2, label=f'最大值: {max_rating:.2f}')
plt.axvline(min_rating, color='red', linestyle='dashed', linewidth=2, label=f'最小值: {min_rating:.2f}')
plt.legend(loc='upper right')
plt.title('評分分佈情況', size="large", fontweight="bold")
plt.xlabel('評分')
plt.ylabel('數量')

# 顯示圖表
plt.show()

# 2. 價格分析
plt.figure(figsize=(12, 8))
mean_price = df_all["價錢"].mean()
max_price = df_all["價錢"].max()
min_price = df_all["價錢"].min()

sns.kdeplot(df_all["價錢"], fill=True, color=colors[2])
plt.axvline(mean_price, color='blue', linestyle='dashed', linewidth=2, label=f'平均: {mean_price:.2f}')
plt.axvline(max_price, color='green', linestyle='dashed', linewidth=2, label=f'最大值: {max_price:.2f}')
plt.axvline(min_price, color='red', linestyle='dashed', linewidth=2, label=f'最小值: {min_price:.2f}')
plt.legend(loc='upper right')
plt.title('價格分佈情況', size="large", fontweight="bold")
plt.xlabel('價錢')
plt.ylabel('密度')

plt.show()

# 3. 評論數量分析
plt.figure(figsize=(12, 8))
mean_comment_count = df_all["評論數量"].mean()
max_comment_count = df_all["評論數量"].max()
min_comment_count = df_all["評論數量"].min()

sns.histplot(df_all["評論數量"], bins=20, kde=True, color=colors[3])
plt.axvline(mean_comment_count, color='blue', linestyle='dashed', linewidth=2, label=f'平均: {mean_comment_count:.2f}')
plt.axvline(max_comment_count, color='green', linestyle='dashed', linewidth=2, label=f'最大值: {max_comment_count:.2f}')
plt.axvline(min_comment_count, color='red', linestyle='dashed', linewidth=2, label=f'最小值: {min_comment_count:.2f}')
plt.legend(loc='upper right')
plt.title('評論數量分佈情況', size="large", fontweight="bold")
plt.xlabel('評論數量')
plt.ylabel('數量')

# 顯示圖表
plt.show()

# 繪製季度商品數量柱狀圖

# 將上市日期轉換為 datetime 格式
df_all['上市日期'] = pd.to_datetime(df_all['上市日期'], errors='coerce')

# 提取年份和季度作為新的欄位
df_all['年份'] = df_all['上市日期'].dt.year
df_all['季度'] = df_all['上市日期'].dt.quarter

# 計算每個季度的商品數量
product_count_by_quarter = df_all.groupby(['年份', '季度']).size().reset_index(name='商品數量')

# 計算每年的商品數量
product_count_by_year = df_all.groupby('年份').size().reset_index(name='商品數量')

plt.figure(figsize=(12, 8))
sns.barplot(data=product_count_by_quarter, x='季度', y='商品數量', hue='年份', palette='pastel')
plt.title('季度商品數量及年度趨勢', size="large", fontweight="bold")
plt.xlabel('季度')
plt.ylabel('商品數量')

# 顯示圖例
plt.legend(title='年份', loc='upper right')

# 顯示圖表
plt.xticks(range(1, 5))  # 季度從1到4
plt.tight_layout()  # 自動調整圖表布局以避免重疊
plt.grid(True)  # 顯示網格

# 創建第二個子圖，繪製年度商品數量折線圖
plt.subplot(212)
sns.lineplot(data=product_count_by_year, x='年份', y='商品數量', marker='o', color='black')
plt.title('年度商品數量趨勢', size="large", fontweight="bold")
plt.xlabel('年份')
plt.ylabel('商品數量')

# 顯示圖表
plt.tight_layout()
plt.show()

