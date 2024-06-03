import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 連線資料庫
conn = sqlite3.connect(r"C:\Users\student\Desktop\cosme_project\cosme_py\cosme.db")
print("連線成功!")

# 查詢並轉換為 DataFrame
df_all = pd.read_sql('SELECT * FROM cosme_all', conn)
df_highend_beauty = pd.read_sql('SELECT * FROM cosme_highend_beauty', conn)
df_highend_care = pd.read_sql('SELECT * FROM cosme_highend_care', conn)

# 關閉連接
conn.close()

# 設定中文(影響整個程式) "微軟正黑體Microsoft JhengHei"
plt.rcParams["font.family"] = "Microsoft JhengHei"
plt.rcParams["font.size"] = 20
plt.rcParams["axes.unicode_minus"] = False

# 使用 Seaborn 的調色板
colors = sns.color_palette('pastel')

# 計算整體平均評分
overall_avg_score = df_all['評分'].mean()

# 計算平均評分高於整體平均評分的品牌
high_avg_score_brands = df_all.groupby('品牌名稱')['評分'].mean().loc[lambda x: x > overall_avg_score]
high_avg_score_brands = high_avg_score_brands.sort_values(ascending=False)

# 添加專櫃/開架標籤
df_all['開架/專櫃'] = '開架'
df_all.loc[df_all['品牌名稱'].isin(df_highend_beauty['品牌名稱']), '開架/專櫃'] = '專櫃'
df_all.loc[df_all['品牌名稱'].isin(df_highend_care['品牌名稱']), '開架/專櫃'] = '專櫃'

# 繪製高評分品牌的橫向柱狀圖
plt.figure(figsize=(10, 10))
bars = sns.barplot(x=high_avg_score_brands.values, y=high_avg_score_brands.index, palette='pastel')
plt.title('平均評分高於整體平均評分的品牌', fontweight="bold")
plt.xlabel('平均評分')
plt.ylabel('')
plt.xlim(0, 10)

# 添加資料標籤
for bar in bars.containers[0]:
    plt.text(bar.get_width(), bar.get_y() + bar.get_height() / 2, f'{bar.get_width():.2f}', 
             ha='left', va='center', fontsize=20)

plt.show()

# 繪製高評分品牌的專櫃/開架比例及平均評分
high_avg_brands = df_all[df_all['品牌名稱'].isin(high_avg_score_brands.index)]
high_avg_brands_count = high_avg_brands['開架/專櫃'].value_counts()
high_avg_brands_avg_score = high_avg_brands.groupby('開架/專櫃')['評分'].mean()

plt.figure(figsize=(12, 10))
bars = sns.barplot(x=high_avg_brands_count.index, y=high_avg_brands_count.values, palette='pastel', width=0.3)
plt.title('高評分品牌的專櫃/開架比例及平均評分', fontweight="bold")
plt.xlabel('類別')
plt.ylabel('數量')

# 添加數量標籤
for index, value in enumerate(high_avg_brands_count.values):
    plt.text(index, value, str(value), ha='center', va='bottom', fontsize=20)

# 添加平均評分標籤，將其向上移動一點
for index, value in enumerate(high_avg_brands_avg_score.values):
    plt.text(index, high_avg_brands_count.values[index] - 3, f'平均評分: {value:.2f}', 
             ha='center', va='bottom', fontsize=25, color='black')

plt.show()

# 繪製高評分品牌的價錢與評分分布圖
plt.figure(figsize=(12, 10))
sns.scatterplot(x='價錢', y='評分', data=high_avg_brands, hue='開架/專櫃', palette='pastel', s=100)
plt.title('高評分品牌的價錢與評分分布', fontweight="bold")
plt.xlabel('價錢')
plt.ylabel('評分')
plt.show()

# 品牌市場份額分析
brand_counts = df_all['品牌名稱'].value_counts()
top_brands = brand_counts.head(10)

# 繪製品牌市場佔有率 (橫向長條圖)
plt.figure(figsize=(10, 10))
sns.barplot(x=top_brands.values, y=top_brands.index, palette='pastel')
plt.title('品牌市場佔有率 TOP 10', fontweight="bold")
plt.xlabel('商品數量')
plt.ylabel('')
plt.show()

# 計算專櫃/開架的數量及平均評分
all_brands_count = df_all['開架/專櫃'].value_counts()
all_brands_avg_score = df_all.groupby('開架/專櫃')['評分'].mean()

plt.figure(figsize=(12, 10))
bars = sns.barplot(x=all_brands_count.index, y=all_brands_count.values, palette='pastel', width=0.3)
plt.title('排行榜的專櫃/開架比例及平均評分', fontweight="bold")
plt.xlabel('類別')
plt.ylabel('數量')

# 添加數量標籤
for index, value in enumerate(all_brands_count.values):
    plt.text(index, value, str(value), ha='center', va='bottom', fontsize=20)

# 添加平均評分標籤，將其向上移動一點
for index, value in enumerate(all_brands_avg_score.values):
    plt.text(index, all_brands_count.values[index] - 3, f'平均評分: {value:.2f}', 
             ha='center', va='bottom', fontsize=25, color='black')
plt.show()