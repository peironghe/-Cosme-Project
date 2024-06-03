import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# 連線資料庫
conn = sqlite3.connect(r"C:\Users\student\Desktop\cosme_project\cosme_py\cosme.db")
print("連線成功!")

# 查詢並轉換為 DataFrame
df_goodbuy = pd.read_sql('SELECT * FROM cosme_goodbuy', conn)

# 關閉連接
conn.close()

# 設定中文字體
plt.rcParams["font.family"] = "Microsoft JhengHei"
plt.rcParams["font.size"] = 20
plt.rcParams["axes.unicode_minus"] = False

# 設定DataFrame資料的相關分析
# 計算相關係數矩陣
correlation_matrix = df_goodbuy[['cosme指數', '人氣投票', '銷售數量', '評論數量']].corr()

# 繪製相關矩陣熱圖
plt.figure(figsize=(10, 8))
heatmap = plt.imshow(correlation_matrix, cmap='coolwarm', vmin=-1, vmax=1)

# 添加相關係數的註釋
for i in range(len(correlation_matrix)):
    for j in range(len(correlation_matrix)):
        plt.text(j, i, f"{correlation_matrix.iloc[i, j]:.2f}", ha='center', va='center', color='black')

plt.title('各欄位之間的相關係數', pad=20, fontweight="bold")
plt.xticks(range(len(correlation_matrix)), correlation_matrix.columns, rotation=45)
plt.yticks(range(len(correlation_matrix)), correlation_matrix.index)
plt.colorbar(heatmap, label='相關係數')
plt.tight_layout()
plt.show()

print(correlation_matrix)
