# 排行榜爬蟲
# 匯入套件
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pandas as pd
import time

# 定義爬蟲函數
def crawl_data(url, csv_filename):
    # 取得資料
    ranking_text = ['1', '2', '3']
    product_brand = []
    product_name = []
    product_url = []
    product_price = []
    product_star = []
    launch_date = []
    comment_num = []

    # 爬蟲網頁
    driver = webdriver.Chrome()
    driver.implicitly_wait(5)
    driver.get(url)
    time.sleep(10)

    # 定義頁面
    page_current = 1

    # 使用BeautifulSoup解析網頁    
    soup = BeautifulSoup(driver.page_source, "lxml")

    # ranking_text
    get_ranking_text = soup.find_all('div', class_='ranking-text')
    for i in get_ranking_text:
        rank = i.text.strip()  # 移除可能存在的空格
        if rank:
            ranking_text.append(rank)  

    # product_brand
    get_product_brand = soup.find_all('div', class_='brand-name')
    for i in get_product_brand:
        brand = i.text.strip()  # 移除可能存在的空格
        if brand:
            product_brand.append(brand)  

    # product_name
    get_product_name = soup.find_all('h3', class_='single-dot')  
    for i in get_product_name:
        name = i.text.strip()  # 移除可能存在的空格
        if name:
            product_name.append(name) 
            
    # launch_date ＆ product_price
    get_product_price = soup.find_all('div', class_='product-market-date')  
    for i in get_product_price:
        # 找到包含上市日期和價格的所有<span>元素
        spans = i.find_all('span')
        # 找每個<span>元素
        launch_date_text = ''
        price_text = ''
        for span in spans:
            text = span.text
            if '上市日期' in text:
                # 提取上市日期的數字部分
                launch_date_text = text.split('：')[1]
            elif '價格' in text:
                # 提取價格的數字部分
                price_text = text.split('：')[1]
        # 將上市日期和價格的數字部分轉換為相應的數值型別並添加到相應的列表中
        if launch_date_text:  # 檢查文字是否為空
            launch_date.append(launch_date_text)
        else:
            launch_date.append('None')  # 如果文字為空，添加 None
        if price_text:  # 檢查文字是否為空
            if '/' in price_text:
                price_text = text.split('/')[-1]
                product_price.append(price_text)
            else:
                product_price.append(price_text)
        else:
            product_price.append('None')  # 如果文字為空，添加 None

    # product_star
    get_product_star = soup.find_all('div', class_='product-score-tip')  
    for i in get_product_star:
        score_text = i.text.strip()
        if score_text:  # 檢查文字是否為空
            score_text = score_text.split('：')[1]    
            product_star.append(float(score_text))
        else:
            product_star.append(None)  # 如果文字為空，添加 None
            
    # product_url
    get_product_divs = soup.find_all('div', class_='product-image')  
    for div in get_product_divs[0:50]:
        # 獲取每個 <div> 元素內的第一個 <img> 元素
        first_img = div.find('img')
        if first_img:
            src = first_img.get('src')
            if src:  # 檢查 src 屬性是否存在且不為空
                product_url.append(src)
        
    # comment_num 
    get_comment_num = soup.find_all('div', class_='product-review-count')  
    for i in get_comment_num:
        comment_text = i.text.strip()  # 移除可能存在的空格
        # 從文字中提取數字部分
        comment_number = ''.join(filter(str.isdigit, comment_text))
        if comment_number:
            comment_num.append(int(comment_number))

    # 跳轉頁面爬取全部資料
    try:
        next_button = driver.find_element(By.XPATH, '//div[@class="uc-tag-ranking-pagnation"]//div[@data-page="{}"]'.format(page_current + 1))
        next_button.click()
        page_current += 1
        time.sleep(10)  # 等待頁面加載
    except Exception as e:
        print("無法點擊下一頁按鈕:", e)

    # 資料處理
    df = pd.DataFrame({'排名': ranking_text,
                       '品牌名稱': product_brand,
                       '商品名稱': product_name,
                       '價錢': product_price[0:50],
                       '評分': product_star,
                       '上市日期': launch_date[0:50],
                       '評論數量': comment_num,
                       '商品圖片': product_url})
    # 存csv
    df.to_csv(csv_filename, index=False, encoding='utf_8_sig')

    print(f"{url} 的資料已成功存入 {csv_filename}")
    driver.close()

# 設定要爬取的 URL 和 CSV 檔名
urls = ["https://www.cosme.net.tw/integrated-rankings",
        "https://www.cosme.net.tw/tags/978/ranking",
        "https://www.cosme.net.tw/tags/977/ranking",
        "https://www.cosme.net.tw/tags/967/ranking",
        "https://www.cosme.net.tw/tags/968/ranking",
        "https://www.cosme.net.tw/tags/622/ranking",
        "https://www.cosme.net.tw/tags/623/ranking"]

csv_filenames = ["cosme_all.csv",
                 "cosme_drugstore_beauty.csv",
                 "cosme_drugstore_care.csv",
                 "cosme_highend_beauty.csv",
                 "cosme_highend_care.csv",
                 "cosme_japan.csv",
                 "cosme_korea.csv"]

# 爬取資料
for url, csv_filename in zip(urls, csv_filenames):
    crawl_data(url, csv_filename)

print("已完成，程式結束")


