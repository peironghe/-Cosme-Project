import sqlite3
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

# 連線資料庫
conn = sqlite3.connect(r"C:\Users\student\Desktop\cosme_project\cosme_py\cosme.db")
print("連線成功!")

# 查詢並轉換為 DataFrame
df_all = pd.read_sql('SELECT * FROM cosme_all', conn)

# 關閉連接
conn.close()

# 設定中文(影響整個程式) "微軟正黑體Microsoft JhengHei"
plt.rcParams["font.family"] = "Microsoft JhengHei"
plt.rcParams["font.size"] = 25
plt.rcParams["axes.unicode_minus"] = False

# 使用Seaborn的調色板
colors = sns.color_palette('pastel')

# 散點圖和線性回歸
def scatterplot_with_regression(x, y, data, xlabel, ylabel, title, ax):
    sns.scatterplot(x=x, y=y, data=data, ax=ax)
    ax.set_title(title, size="large", fontweight="bold")
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_ylim(0, 10)  # 設定評分範圍從0到10分

    # 執行線性回歸
    model = LinearRegression()
    X = data[[x]]
    y = data[y]
    model.fit(X, y)

    # 繪製回歸線
    ax.plot(X, model.predict(X), color='red', linewidth=2)

    # 顯示回歸方程式
    ax.text(0.5, 0.85, f'斜率: {model.coef_[0]:.2f}\n截距: {model.intercept_:.2f}\nR-squared: {model.score(X, y):.2f}', 
             horizontalalignment='center', verticalalignment='center', transform=ax.transAxes)
    print(f'斜率: {model.coef_[0]:.2f}\n截距: {model.intercept_:.2f}\nR-squared: {model.score(X, y):.2f}')

# 建立一個橫向排列的大圖表
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 10), gridspec_kw={'width_ratios': [1, 1]})

# 添加大標題
fig.suptitle('綜合美妝排行榜 - 評分', size="x-large", fontweight="bold")

# 第一個子圖: 價錢與評分的關係
scatterplot_with_regression('價錢', '評分', df_all, '價錢', '評分', '價錢與評分的關係', ax1)

# 第二個子圖: 評論數量與評分的關係
scatterplot_with_regression('評論數量', '評分', df_all, '評論數量', '評分', '評論數量與評分的關係', ax2)
ax2.set_ylabel('')  # 隱藏 y 軸

# 自動調整子圖之間間距 left, bottom, right, top = rect
plt.tight_layout(rect=[0, 0, 0.96, 0.96])

# 儲存圖片
plt.savefig('綜合美妝_回歸圖.png')

plt.show()
