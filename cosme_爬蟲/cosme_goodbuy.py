# 必敗爬蟲
# 匯入套件
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pandas as pd
import time

# 取得資料
product_brand = []
product_name = []
product_star = []
product_hit = []
product_sale = []
comment_num = []
product_url = []

# 爬蟲網頁
driver = webdriver.Chrome()
driver.implicitly_wait(5)
url = "https://www.cosme.net.tw/goodbuy"
driver.get(url)
time.sleep(10)

# 跳轉頁面
pages_remaining = True
page_num = 26
page_current = 1

while pages_remaining:
    # 使用BeautifulSoup解析網頁    
    soup = BeautifulSoup(driver.page_source, "lxml")

    # product_brand & name
    get_product_brand_name = soup.find_all('div', class_='title-product-name')
    for i in get_product_brand_name:
        brand_and_name = i.text.strip().split('[')[1]  # 去除所有[]
        brand = brand_and_name.split('] ')[0]
        product_brand.append(brand)
        name = brand_and_name.split('] ')[1]
        product_name.append(name)

    # product_star
    get_product_star = soup.find_all('div', class_='card-product-score')  
    for i in get_product_star:
        score_text = i.text.strip()
        if score_text:  # 檢查文字是否為空
            score_text = score_text.split(' ')[1]    
            product_star.append(float(score_text))
        else:
            product_star.append(None)  # 如果文字為空，添加 None
     
    # product_hit
    get_product_hit = soup.find_all('div', class_='card-pageview')  
    for i in get_product_hit:
        hit_text = i.text.strip()
        if hit_text:  # 檢查文字是否為空
            hit_text = hit_text.split(' ')[0]    
            product_hit.append(hit_text)
        else:
            product_hit.append(None)  # 如果文字為空，添加 None
                
    # product_sale
    get_product_sale = soup.find_all('div', class_='button-num')  
    for i in get_product_sale:
        sale_text = i.text.strip()
        if sale_text:  # 檢查文字是否為空
            product_sale.append(sale_text)
        else:
            product_sale.append(None)  # 如果文字為空，添加 None
        
    # comment_num 
    get_comment_num = soup.find_all('div', class_='review-count')  
    for i in get_comment_num:
        comment_text = i.text.strip()  # 移除可能存在的空格
        # 從文字中提取數字部分
        comment_number = ''.join(filter(str.isdigit, comment_text))
        if comment_number:
            comment_num.append(str(comment_number))
                
    # product_url
    get_product_url = driver.find_elements(By.CSS_SELECTOR, "img.img-auto-center")
    for i in get_product_url[8:28]:
        src = i.get_attribute('src')
        if src:  # 檢查 src 屬性是否存在且不為空
            product_url.append(src)
    
    # 換頁         
    try:
        #自動按下一頁按鈕
        next_link=driver.find_element(By.CSS_SELECTOR,'a.next_page')
        next_link.click()
        time.sleep(10)
        if page_current < page_num :
            page_current = page_current + 1
        else:
            pages_remaining = False
    except Exception as e:
        pages_remaining = False
        print("無法點擊下一頁按鈕:", e)

# 資料處理
df = pd.DataFrame({'品牌名稱': product_brand,
                   '商品名稱': product_name,
                   'cosme指數': product_star,
                   '人氣投票': product_hit,
                   '銷售數量': product_sale,                   
                   '評論數量': comment_num,
                   '商品圖片': product_url})
# 存csv
df.to_csv("cosme_goodbuy.csv", index=False, encoding='utf_8_sig')
        
print("已完成 程式結束")
driver.close()