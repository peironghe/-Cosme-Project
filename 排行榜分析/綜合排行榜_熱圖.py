import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

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

# 將上市日期轉換為 datetime 格式
df_all['上市日期'] = pd.to_datetime(df_all['上市日期'], errors='coerce')

# 提取上市年份作為新的欄位
df_all['上市年份'] = df_all['上市日期'].dt.year

# 將上市季度轉換為數值
df_all['上市季度'] = df_all['上市日期'].dt.quarter

# 選擇需要的欄位
columns_of_interest = ['排名', '價錢', '評分', '評論數量', '上市季度', '上市年份']
df_selected = df_all[columns_of_interest]

# 計算相關係數矩陣
correlation_matrix = df_selected.corr()

# 繪製相關矩陣熱圖
plt.figure(figsize=(10, 8))
heatmap = plt.imshow(correlation_matrix, cmap='coolwarm', vmin=-1, vmax=1)

# 添加相關係數的註釋
for i in range(len(columns_of_interest)):
    for j in range(len(columns_of_interest)):
        plt.text(j, i, f"{correlation_matrix.iloc[i, j]:.2f}", ha='center', va='center', color='black')

plt.title('各欄位之間的相關係數', pad=20, fontweight="bold")
plt.xticks(range(len(columns_of_interest)), columns_of_interest, rotation=45)
plt.yticks(range(len(columns_of_interest)), columns_of_interest)
plt.colorbar(heatmap, label='相關係數')
plt.tight_layout()
plt.show()

print(correlation_matrix)
