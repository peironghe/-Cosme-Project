import sqlite3
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# 連線資料庫
conn = sqlite3.connect(r"C:\Users\student\Desktop\cosme_project\cosme_py\cosme.db")
print("連線成功!")

# 查詢並轉換為 DataFrame
df_goodbuy = pd.read_sql('SELECT * FROM cosme_goodbuy', conn)

# 關閉連接
conn.close()

# 設定中文(影響整個程式) "微軟正黑體Microsoft JhengHei"
plt.rcParams["font.family"] = "Microsoft JhengHei"
plt.rcParams["font.size"] = 20
plt.rcParams["axes.unicode_minus"] = False

# 使用Seaborn的調色板
colors = sns.color_palette('pastel')

# 計算品牌的總銷量
brand_sales = df_goodbuy.groupby('品牌名稱')['銷售數量'].sum().reset_index()

# 計算前十名品牌的銷售數量
top_brands = brand_sales.sort_values(by='銷售數量', ascending=False).head(10)

# 繪製前十名品牌的總銷量橫向條形圖
plt.figure(figsize=(12, 8))  
ax = sns.barplot(x='銷售數量', y='品牌名稱', data=top_brands, palette=colors, orient='h')
plt.title('品牌銷量 TOP10', fontweight="bold")
plt.xlabel('總銷量')
plt.ylabel('')

# 添加資料標籤
for index, value in enumerate(top_brands['銷售數量']):
    plt.text(value, index, str(int(value)), fontsize=20, va='center')

plt.show()

# 計算品牌的人氣投票
brand_popularity = df_goodbuy.groupby('品牌名稱')['人氣投票'].sum().reset_index()

# 計算前十名品牌的人氣投票
top_popular_brands = brand_popularity.sort_values(by='人氣投票', ascending=False).head(10)

# 繪製前十名品牌的人氣投票橫向條形圖
plt.figure(figsize=(12, 8))
ax = sns.barplot(x='人氣投票', y='品牌名稱', data=top_popular_brands, palette=colors, orient='h')
plt.title('品牌人氣 TOP10', fontweight="bold")
plt.xlabel('人氣投票')
plt.ylabel('')

# 添加資料標籤
for index, value in enumerate(top_popular_brands['人氣投票']):
    plt.text(value, index, str(int(value)), fontsize=20, va='center')

plt.show()

# 計算品牌的平均評分
brand_avg_rating = df_goodbuy.groupby('品牌名稱')['cosme指數'].mean().reset_index()

# 計算前十名品牌的平均評分
top_avg_rating_brands = brand_avg_rating.sort_values(by='cosme指數', ascending=False).head(10)

# 繪製前十名品牌的平均評分橫向條形圖
plt.figure(figsize=(12, 8))
ax = sns.barplot(x='cosme指數', y='品牌名稱', data=top_avg_rating_brands, palette=colors, orient='h')
plt.title('品牌平均評分 TOP10', fontweight="bold")
plt.xlabel('平均評分')
plt.ylabel('')

# 添加資料標籤
for index, value in enumerate(top_avg_rating_brands['cosme指數']):
    plt.text(value, index, f'{value:.2f}', fontsize=20, va='center')

plt.show()

# 計算品牌的評論數量
brand_comments = df_goodbuy.groupby('品牌名稱')['評論數量'].sum().reset_index()

# 計算前十名品牌的評論數量
top_comment_brands = brand_comments.sort_values(by='評論數量', ascending=False).head(10)

# 繪製前十名品牌的評論數量橫向條形圖
plt.figure(figsize=(12, 8))
ax = sns.barplot(x='評論數量', y='品牌名稱', data=top_comment_brands, palette=colors, orient='h')
plt.title('品牌評論數量 TOP10', fontweight="bold")
plt.xlabel('評論數量')
plt.ylabel('')

# 添加資料標籤
for index, value in enumerate(top_comment_brands['評論數量']):
    plt.text(value, index, str(int(value)), fontsize=20, va='center')

plt.show()

from collections import Counter

# 計算品牌出現在各個 TOP10 中的次數
brand_counts = Counter(top_brands['品牌名稱']) + Counter(top_popular_brands['品牌名稱']) + Counter(top_avg_rating_brands['品牌名稱']) + Counter(top_comment_brands['品牌名稱'])

# 找出至少出現兩次的品牌
repeated_brands = [brand for brand, count in brand_counts.items() if count >= 2]
print("重複出現在至少兩張 TOP10 的品牌：", repeated_brands)





