#!/usr/bin/env python
# coding: utf-8

# In[15]:


# 觀察搜尋結果網址,用網址切換頁數
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time
from bs4 import BeautifulSoup
from selenium.webdriver import ActionChains
import csv
s = Service("./chromedriver.exe")
driver = webdriver.Chrome(service=s)
driver.get("https://www.yes123.com.tw/wk_index/joblist.asp?find_key2=%E5%BE%8C%E7%AB%AF%E5%B7%A5%E7%A8%8B%E5%B8%AB&order_ascend=desc&strrec=0&search_key_word=%E5%BE%8C%E7%AB%AF%E5%B7%A5%E7%A8%8B%E5%B8%AB&search_type=job&search_from=joblist")
allkey = driver.page_source
time.sleep(2) 
soup = BeautifulSoup(str(allkey), 'html.parser')
page=soup.find("div",{"id":"select_page_num"}).find_all("option")[:1]
yes123_host = "https://www.yes123.com.tw/wk_index/"
#取出所有頁數的數值
pages=[]
for i in page:    
    allpage_value=int(i.text)
    pages.append(allpage_value)
pages.insert(0,0)
#取出詳細內容的網址
search_links=[]
for search_pagevalue in pages :
    search_link_part="joblist.asp?search_job_t=1&strrec="
    search_link_part2= "&search_key_word=%E5%BE%8C%E7%AB%AF%E5%B7%A5%E7%A8%8B%E5%B8%AB&search_type=job&search_from=joblist"
    search_link = yes123_host+search_link_part+str(search_pagevalue*30)+search_link_part2
    search_links.append(search_link)
search_pagesources=[]
# 取出詳細頁面的內容
for search_pagesource in search_links:
    driver.get(search_pagesource)
    time.sleep(2)
    page_source = driver.page_source
    page_source_soup = BeautifulSoup(str(page_source), 'html.parser')
    search_pagesources.append(page_source_soup)
link_results=[]
results2=[]
# 取出職缺,估僧名稱,公司地址

for search_pagesource in  search_pagesources :   
        job_titlepage_div = search_pagesource.find_all("div",{"class":"Job_opening_item"})
        for link in job_titlepage_div:
            try:
                all_part_links =link.find("h5").find("a").get("href")
                all_title_links = yes123_host+all_part_links  
                link_results.append(all_title_links)
                all_titles = link.find("h5").get_text()
                all_bus= link.find("h6").get_text()
                all_addr=link.find("div",{"class":"Job_opening_item_info"}).find("span").text
                result2 ={
                         '職缺': all_titles,
                        '公司名稱': all_bus,
                        '公司地址': all_addr
                    }
                results2.append(result2)
            except:
                continue
detail_pagesource_results=[] 
#取出page_source
for all_detail_page in link_results:

    driver.get(all_detail_page)
    time.sleep(2)
    onepage_detail_pagesource = driver.page_source
    time.sleep(1) 
    soup2 = BeautifulSoup(str(onepage_detail_pagesource), 'html.parser')   
    detail_pagesource_results.append(soup2)     
driver.close()
all_h3_list =[]
detail_results=[]
#取出對應的資料內容
for new in detail_pagesource_results:         
    test2 = new.find_all("div",{"class":"job_explain"})[1:] 
    h3_results=[]
    for okok in test2:
        h3_result=str(okok.find("h3"))   
        h3_results.append(h3_result)   
    try:
        a=h3_results.index("<h3>工作條件</h3>")
        # print(a)
        test4 = new.find_all("div",{"class":"job_explain"})[a+1].find_all("span",{"class":"right_main"})[0].text
        test3 = new.find_all("div",{"class":"job_explain"})[a+1].find_all("span",{"class":"right_main"})[1].text        
    except:
        test3=" "
        test4=" "
    job_salary_div = new.find("div",{"class":"job_explain mt"}).find_all("span",{"class":"right_main"})[1].text  
    job_content_div = new.find("div",{"class":"job_explain mt"}).find_all("span",{"class":"right_main"})[0].text  
    try:
        b=h3_results.index("<h3>技能與求職專長</h3>")
        job_can_div = new.find_all("div",{"class":"job_explain"})[b+1].find_all("span",{"class":"right_main"})
        for i1 in job_can_div:
            job_can_text =i1.text          
    except:
        job_can_text=" "   
    try:
        c=h3_results.index("<h3>其他條件</h3>")
        job_other_div = new.find_all("div",{"class":"job_explain"})[c+1].find_all("span",{"class":"exception"})
        for i2 in job_other_div:
            job_other_text=i2.text           
    except:
        job_other_text=" "      
    detail_result ={
             '學歷': test4,
            '科系': test3,
            '薪資':  job_salary_div,
            '工作內容':job_content_div,
            '擅長工具':job_can_text,
            '其他條件':job_other_text
        }
    detail_results.append(detail_result)
#所有所需資訊合併成桐一個list
for i in range(min(len(detail_results),len(results2))):
    detail_results[i].update(results2[i])   
# 輸出成csv
labels =  ['職缺','公司名稱','公司地址','學歷','科系','薪資','工作內容','擅長工具','其他條件']
dct_arr = detail_results
try:
    with open('03page_all_column.csv', 'w',encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=labels)
        writer.writeheader()
        for elem in dct_arr:
            writer.writerow(elem)
except IOError:
     print("I/O error")


# In[ ]:




