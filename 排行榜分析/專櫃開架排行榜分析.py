import sqlite3
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# 連線資料庫
conn = sqlite3.connect(r"C:\Users\student\Desktop\cosme_project\cosme_py\cosme.db")
print("連線成功!")

# 查詢並轉換為 DataFrame
df_highend_beauty = pd.read_sql('SELECT * FROM cosme_highend_beauty', conn)
df_drugstore_beauty = pd.read_sql('SELECT * FROM cosme_drugstore_beauty', conn)

# 關閉連接
conn.close()

# 設定中文(影響整個程式) "微軟正黑體Microsoft JhengHei"
plt.rcParams["font.family"] = "Microsoft JhengHei"
plt.rcParams["font.size"] = 20
plt.rcParams["axes.unicode_minus"] = False

# 使用Seaborn的調色板
colors = sns.color_palette('pastel')

# 1. 品牌佔比分析
plt.figure(figsize=(20, 10), constrained_layout=True)
plt.subplot(1, 2, 1, aspect='equal')
brand_counts_highend = df_highend_beauty['品牌名稱'].value_counts()
top_5_brands_highend = brand_counts_highend.head(5)
other_count_highend = brand_counts_highend[5:].sum()
top_5_brands_highend['其他'] = other_count_highend
plt.pie(top_5_brands_highend, labels=top_5_brands_highend.index, autopct='%1.1f%%', startangle=140, colors=colors)
plt.title('專櫃排行榜品牌市佔比', size="x-large", fontweight="bold")

plt.subplot(1, 2, 2, aspect='equal')
brand_counts_drugstore = df_drugstore_beauty['品牌名稱'].value_counts()
top_5_brands_drugstore = brand_counts_drugstore.head(5)
other_count_drugstore = brand_counts_drugstore[5:].sum()
top_5_brands_drugstore['其他'] = other_count_drugstore
plt.pie(top_5_brands_drugstore, labels=top_5_brands_drugstore.index, autopct='%1.1f%%', startangle=140, colors=colors)
plt.title('開架排行榜品牌市佔比', size="x-large", fontweight="bold")

# 顯示圖表
plt.show()

# 2. 評分分析
plt.figure(figsize=(20, 10))
plt.subplot(1, 2, 1)
mean_rating_highend = df_highend_beauty["評分"].mean()
max_rating_highend = df_highend_beauty["評分"].max()
min_rating_highend = df_highend_beauty["評分"].min()

sns.histplot(df_highend_beauty["評分"], bins=20, kde=True, color=colors[1])
plt.axvline(mean_rating_highend, color='blue', linestyle='dashed', linewidth=2, label=f'平均: {mean_rating_highend:.2f}')
plt.axvline(max_rating_highend, color='green', linestyle='dashed', linewidth=2, label=f'最大值: {max_rating_highend:.2f}')
plt.axvline(min_rating_highend, color='red', linestyle='dashed', linewidth=2, label=f'最小值: {min_rating_highend:.2f}')
plt.legend(loc='upper right')
plt.title('專櫃排行榜評分分佈情況', size="x-large", fontweight="bold")
plt.xlabel('評分')
plt.ylabel('數量')

plt.subplot(1, 2, 2)
mean_rating_drugstore = df_drugstore_beauty["評分"].mean()
max_rating_drugstore = df_drugstore_beauty["評分"].max()
min_rating_drugstore = df_drugstore_beauty["評分"].min()

sns.histplot(df_drugstore_beauty["評分"], bins=20, kde=True, color=colors[1])
plt.axvline(mean_rating_drugstore, color='blue', linestyle='dashed', linewidth=2, label=f'平均: {mean_rating_drugstore:.2f}')
plt.axvline(max_rating_drugstore, color='green', linestyle='dashed', linewidth=2, label=f'最大值: {max_rating_drugstore:.2f}')
plt.axvline(min_rating_drugstore, color='red', linestyle='dashed', linewidth=2, label=f'最小值: {min_rating_drugstore:.2f}')
plt.legend(loc='upper right')
plt.title('開架排行榜評分分佈情況', size="x-large", fontweight="bold")
plt.xlabel('評分')
plt.ylabel('數量')

# 自動調整子圖之間間距
plt.tight_layout(rect=[0, 0, 1, 0.96])

# 顯示圖表
plt.show()

# 3. 價格分析
plt.figure(figsize=(20, 10))
plt.subplot(1, 2, 1)
mean_price_highend = df_highend_beauty["價錢"].mean()
max_price_highend = df_highend_beauty["價錢"].max()
min_price_highend = df_highend_beauty["價錢"].min()

sns.kdeplot(df_highend_beauty["價錢"], fill=True, color=colors[2])
plt.axvline(mean_price_highend, color='blue', linestyle='dashed', linewidth=2, label=f'平均: {mean_price_highend:.2f}')
plt.axvline(max_price_highend, color='green', linestyle='dashed', linewidth=2, label=f'最大值: {max_price_highend:.2f}')
plt.axvline(min_price_highend, color='red', linestyle='dashed', linewidth=2, label=f'最小值: {min_price_highend:.2f}')
plt.legend(loc='upper right')
plt.title('專櫃排行榜價格分佈情況', size="x-large", fontweight="bold")
plt.xlabel('價錢')
plt.ylabel('密度')

plt.subplot(1, 2, 2)
mean_price_drugstore = df_drugstore_beauty["價錢"].mean()
max_price_drugstore = df_drugstore_beauty["價錢"].max()
min_price_drugstore = df_drugstore_beauty["價錢"].min()

sns.kdeplot(df_drugstore_beauty["價錢"], fill=True, color=colors[2])
plt.axvline(mean_price_drugstore, color='blue', linestyle='dashed', linewidth=2, label=f'平均: {mean_price_drugstore:.2f}')
plt.axvline(max_price_drugstore, color='green', linestyle='dashed', linewidth=2, label=f'最大值: {max_price_drugstore:.2f}')
plt.axvline(min_price_drugstore, color='red', linestyle='dashed', linewidth=2, label=f'最小值: {min_price_drugstore:.2f}')
plt.legend(loc='upper right')
plt.title('開架排行榜價格分佈情況', size="x-large", fontweight="bold")
plt.xlabel('價錢')
plt.ylabel('密度')

# 自動調整子圖之間間距
plt.tight_layout(rect=[0, 0, 1, 0.96])

# 顯示圖表
plt.show()

