import sqlite3
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import urllib.request
from PIL import Image

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

# 合併品牌名稱和產品名稱，計算每個產品的總銷量
df_goodbuy['品牌和產品名稱'] = df_goodbuy['品牌名稱'] + ' - ' + df_goodbuy['商品名稱']
product_sales = df_goodbuy.groupby('品牌和產品名稱')['銷售數量'].sum().reset_index()

# 計算前十名產品的銷售數量
top_products = product_sales.sort_values(by='銷售數量', ascending=False).head(10)

# 繪製前十名產品的總銷量橫向條形圖
plt.figure(figsize=(12, 8))  
ax = sns.barplot(x='銷售數量', y='品牌和產品名稱', palette=colors, data=top_products, orient='h')
plt.title('商品銷量 TOP10', fontweight="bold")
plt.xlabel('總銷量')
plt.ylabel('')

# 添加資料標籤
for index, value in enumerate(top_products['銷售數量']):
    plt.text(value, index, str(int(value)), fontsize=20, va='center')

plt.show()

# 假設 df_goodbuy 包含了產品名稱和圖片網址的數據
# 我們先選擇前十名產品
top_products_images = df_goodbuy.nlargest(10, '銷售數量')

# 設置子圖的行和列數
rows = 2
cols = 5

# 創建子圖
fig, axes = plt.subplots(rows, cols, figsize=(18, 9))

# 前十名產品
for i, (index, row) in enumerate(top_products_images.iterrows()):
    url = row['商品圖片']
    image = Image.open(urllib.request.urlopen(url))
    
    # 確定子圖的索引
    r = i // cols
    c = i % cols
    
    # 在相應的子圖中顯示圖片和排名
    axes[r, c].imshow(image)
    axes[r, c].set_title(f'#{i+1}\n{row["品牌名稱"]}\n{row["商品名稱"]}', fontsize=20)
    axes[r, c].axis('off')

# 調整子圖的間距
fig.subplots_adjust(wspace=0.4, hspace=0.6)
plt.tight_layout(rect=[0,0,0.9,0.96])
plt.show()
