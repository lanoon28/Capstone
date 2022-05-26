import requests
import time
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver


class crawling:
    def __init__(self):
        self.url = ''
        self.ids_html = ''
        self.comments_html = ''

    def urlget(self):
        return self.url

    def crawdata(self, Url):

        self.url = Url
        self.driver = webdriver.Chrome("./chromedriver")

        self.options = webdriver.ChromeOptions()
        self.options.add_argument('headless')
        self.options.add_argument("disable-gpu")
        #self.options.add_argument('window-size=1080x720')
        self.driver.set_window_size(900,600)

        self.driver.get(self.url)
        time.sleep(3)

        self.body = self.driver.find_element_by_tag_name('body')
        self.last_page_height = self.driver.execute_script("return document.documentElement.scrollHeight")

        while True:
            self.driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
            time.sleep(3)
            self.new_page_height = self.driver.execute_script("return document.documentElement.scrollHeight")

            if self.new_page_height == self.last_page_height:
                break
            self.last_page_height = self.new_page_height

        self.comments_html = self.driver.page_source

        self.driver.quit()

        self.savexl()

    def savexl(self):
        self.comments_soup = BeautifulSoup(self.comments_html, 'lxml')

        self.ids_html = self.comments_soup.select('div#header-author > h3 > #author-text > span')
        self.comments_html = self.comments_soup.select('yt-formatted-string#content-text')

        self.comments_len = len(self.comments_html)
        self.ids_len = len(self.ids_html)

        # comments_len

        # Empty listsel
        self.Ids = []
        self.Comments = []
        self.no = []

        for i in range(self.ids_len):
            self.temp_id = self.ids_html[i].text
            self.temp_id = self.temp_id.replace('\n', '')
            self.temp_id = self.temp_id.replace('\t', '')
            self.temp_id = self.temp_id.replace('    ', '')
            self.Ids.append(self.temp_id)

            self.temp_comment = self.comments_html[i].text
            self.temp_comment = self.temp_comment.replace('\n', '')
            self.temp_comment = self.temp_comment.replace('\t', '')
            self.temp_comment = self.temp_comment.replace('    ', '')
            self.Comments.append(self.temp_comment)

            self.no.append(i)

        self.youtube_df = pd.DataFrame([self.no, self.Ids, self.Comments,], index=['no', 'ID', 'Comment']).T
        self.youtube_df

        self.youtube_df.to_excel('craw.xlsx')


# crtest = crawling()
# url = 'https://www.youtube.com/watch?v=feOYHukDreU'
# crtest.crawdata(url)
# crtest.savexl()
# print(crtest.urlget())
