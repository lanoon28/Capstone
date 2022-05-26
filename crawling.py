import requests
import time
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver

options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('window-size=1920x1080')

url = ''
#https://www.youtube.com/watch?v=0xbefR6KEHc
driver = webdriver.Chrome("./chromedriver")

# Move to url
driver.get(url)
time.sleep(3)

# Scroll down
body = driver.find_element_by_tag_name('body')
last_page_height = driver.execute_script("return document.documentElement.scrollHeight")

while True:
    driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
    time.sleep(3)
    new_page_height = driver.execute_script("return document.documentElement.scrollHeight")

    if new_page_height == last_page_height:
        break
    last_page_height = new_page_height


# Save html code to comments_html
comments_html = driver.page_source

# Quit selenium
driver.quit()

comments_soup = BeautifulSoup(comments_html, 'lxml')

ids_html = comments_soup.select('div#header-author > h3 > #author-text > span')
comments_html = comments_soup.select('yt-formatted-string#content-text')

comments_len = len(comments_html)
ids_len = len(ids_html)

# Empty listsel
Ids = []
Comments = []

for i in range(ids_len):
    temp_id = ids_html[i].text
    temp_id = temp_id.replace('\n', '')
    temp_id = temp_id.replace('\t', '')
    temp_id = temp_id.replace('    ', '')
    Ids.append(temp_id)

    temp_comment = comments_html[i].text
    temp_comment = temp_comment.replace('\n', '')
    temp_comment = temp_comment.replace('\t', '')
    temp_comment = temp_comment.replace('    ', '')
    Comments.append(temp_comment)

youtube_df = pd.DataFrame([Ids, Comments,],index = ['ID', 'Comment']).T

# save to excel
youtube_df.to_excel('craw.xlsx')