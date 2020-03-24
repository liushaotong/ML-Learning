import random
import time
from io import BytesIO

import jieba
import pandas as pd
import requests
from PIL import Image
from lxml import etree


class pachong():
    def __init__(self):
        self.session = requests.session()
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'}
        self.url_login = 'https://www.douban.com/login'
        self.url_comment = 'https://movie.douban.com/subject/26794435/comments?start=%d&limit=20&sort=new_score&status=P'

    def scrapy_(self):
        login_request = self.session.get(self.url_login, headers=self.headers)
        selector = etree.HTML(login_request.content)
        post_data = {'source':'None',
                    'redir':'https://www.douban.com',
                    'form_emial':'19920061241',
                    'form_password':'legend961204',
                    'login':'登录'}
        captcha_img_url = selector.xpath('//img[@id="captcha_image"]/@src')
        if captcha_img_url != []:
            pic_request = requests.get(captcha_img_url[0])
            img = Image.open(BytesIO(pic_request.content))
            img.show()
            string = input('填写验证码：')
            post_data['captcha-solution'] = string
            captcha_id = selector.xpath('//input[@name="captcha-id"]/@value')
            post_data['captcha-id'] = captcha_id[0]

        self.session.post(self.url_login,data=post_data)
        print('已登录豆瓣')

        users = []
        stars = []
        times = []
        comment_texts = []

        for i in range(0, 500, 20):
            data = self.session.get(self.url_comment % i, headers = self.headers)
            print('进度', i, '条', '状态是: ',data.status_code)
            time.sleep(random.random())
            selector = etree.HTML(data.text)
            comments = selector.xpath('//div[@class="comment"]')
            for comment in comments:
                user = comment.xpath('.//h3/span[2]/a/text()')[0]
                star = comment.xpath('.//h3/span[2]/span[2]/@class')[0][7:8]
                date_time = comment.xpath('.//h3/span[2]/span[3]/@title')
                if len(date_time) != 0:
                    date_time = date_time[0]
                else:
                    date_time = None
                comment_text = comment.xpath('.//p/span/text()')[0].strip()
                users.append(user)
                stars.append(star)
                times.append(date_time)
                comment_texts.append(comment_text)

        comment_dic = {'user': users, 'star': stars, 'time': times, 'comments': comment_texts}
        comment_df = pd.DataFrame(comment_dic)
        comment_df.to_csv('duye_comments.csv')
        comment_df['comments'].to_csv('comment.csv', index=False)
        print(comment_df)


    def jibeba_(self):
        content = open('comment.csv', 'r', encoding='utf-8').read()
        word_list = jieba.cut(content)



nezha = pachong()
nezha.scrapy_()