import requests
from requests.exceptions import RequestException
from bs4 import BeautifulSoup
import re
import json
import time

findLink = re.compile(r'<a href="(.*?)">', re.S)
findImgSrc = re.compile(r'<img.*src="(.*?)"', re.S)
findTitle = re.compile(r'<span class="title">(.*)</span>')
findRating = re.compile(r'<span class="rating_num" property="v:average">(.*?)</span>')
findJudge = re.compile(r'<span>(.*?)人评价</span>')
findBd = re.compile(r'<p class="">(.*?)</p>', re.S)
findDir = re.compile(r'导演: (.*?)主演', re.S)
findActor = re.compile(r'主演: (.*?)<br/>', re.S)


class page_spider:

    def __init__(self, url):
        self.url = url
        self.head = {  # 模拟浏览器头部信息，向服务器发送消息
            "User-Agent": "Mozilla / 5.0(Windows NT 10.0;Win64;x64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 83.0.4103.116Safari / 537.36"
        }  #
        self.detail = []

    def get_one_page(self):
        try:
            response = requests.get(self.url, headers=self.head)
            if response.status_code == 200:
                return response.text
            return None
        except RequestException:
            return None

    def parse_one_page(self, html):
        # print(html)
        soup = BeautifulSoup(html, 'lxml')
        # print(soup.prettify())
        for item in soup.find_all('div', class_="item"):
            data = []
            item = str(item)

            link = re.findall(findLink, item)[0]
            data.append(link)

            ImgSrc = re.findall(findImgSrc, item)[0]  # 图片链接
            data.append(ImgSrc)

            Title = re.findall(findTitle, item)[0]  # 片名
            data.append(Title)

            rate = re.findall(findRating, item)[0]
            data.append(rate)

            judge = re.findall(findJudge, item)[0]
            data.append(judge)

            Bd = re.findall(findBd, item)[0]
            Bd = "".join(Bd.split('\xa0'))
            dir = re.search(findDir, Bd)
            if dir is not None:
                dir = dir.group(1)
            else:
                dir = ''
            actor = re.search(findActor, Bd)
            if actor is not None:
                actor = actor.group(1)
            else:
                actor = ''

            temp = re.search(r'[0-9]+.*\/?', Bd).group().split('/')
            year, count, category = temp[0], temp[1], temp[2]

            data.append(dir)
            data.append(actor)
            data.append(year)
            data.append(count)
            data.append(category)

            self.detail.append(data)

    def update_url(self, url):
        self.url = url


def main():
    # baseurl = 'https://movie.douban.com/top250?start='
    baseurl = 'http://www.dianping.com/shop'
    spider = page_spider(baseurl)
    html = spider.get_one_page()
    print(html)
    # for i in range(0, 10):
    #     url = baseurl + str(i * 25)
    #     spider.update_url(url)
    #     print(url)
    #     html = spider.get_one_page()
    #     spider.parse_one_page(html)
    # for item in spider.detail:
    #     print(item)


if __name__ == '__main__':
    main()
