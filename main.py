import requests
from requests.exceptions import RequestException
from bs4 import BeautifulSoup
import re
from selenium import webdriver

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

    def __init__(self, url, user ,passowrd):
        self.user = user
        self.password = passowrd
        self.cookie = 'mtcdn=K; lsu=; _lxsdk_cuid=17cbc59576065-07b5578285d7b6-b7a1438-151800-17cbc595761c8; uuid=921277537fa24939a49f.1635309002.1.0.0; iuuid=957CDB83ADA028D4A9BA71B6A658E27023C124583725054334B678ADCA7131AC; cityname=%E5%B8%B8%E5%B7%9E; webp=1; _lxsdk=957CDB83ADA028D4A9BA71B6A658E27023C124583725054334B678ADCA7131AC; __utma=74597006.1979291095.1635309702.1635309702.1635309702.1; __utmz=74597006.1635309702.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); latlng=26.021646,119.200686,1635309702715; _hc.v=90b07ed2-3aa1-277a-6d79-dee4380e143a.1635309865; i_extend=H__a100001__b1; ci=44; rvct=44%2C1016%2C89%2C10%2C20; u=1046899153; n=epS499638294; lt=GWz4wKHQc9nFsyZNmrUnbBewF1AAAAAACw8AAPMg5sc0ro11_IGLIqI1EQmlsp0E0w_27Y3Z5h9nt3LHF9aVtmlBTZRc6XkDS29OPg; mt_c_token=GWz4wKHQc9nFsyZNmrUnbBewF1AAAAAACw8AAPMg5sc0ro11_IGLIqI1EQmlsp0E0w_27Y3Z5h9nt3LHF9aVtmlBTZRc6XkDS29OPg; token=GWz4wKHQc9nFsyZNmrUnbBewF1AAAAAACw8AAPMg5sc0ro11_IGLIqI1EQmlsp0E0w_27Y3Z5h9nt3LHF9aVtmlBTZRc6XkDS29OPg; token2=GWz4wKHQc9nFsyZNmrUnbBewF1AAAAAACw8AAPMg5sc0ro11_IGLIqI1EQmlsp0E0w_27Y3Z5h9nt3LHF9aVtmlBTZRc6XkDS29OPg; firstTime=1635348363373; unc=epS499638294; __mta=150960009.1635316077198.1635348035597.1635348363776.3; _lxsdk_s=17cc256b51e-213-a97-9f3%7C%7C4'
        self.url = url
        self.head = {  # 模拟浏览器头部信息，向服务器发送消息
            "User-Agent": "Mozilla / 5.0(Windows NT 10.0;Win64;x64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 83.0.4103.116Safari / 537.36"
        }  #
        self.detail = []



    def get_cookies(self):
        browser = webdriver.Chrome()
        browser.get(self.url)
        input = browser.find_element_by_id('login-email')
        input.click()
        time.sleep(1)
        input.send_keys(self.user)
        time.sleep(2)
        input = browser.find_element_by_id('login-password')
        input.click()
        time.sleep(1)
        # input.send_keys(self.password)
        for i in range(0,len(self.password)):
            input.send_keys(self.password[i])
            time.sleep(0.1)

        time.sleep(2)
        input = browser.find_element_by_css_selector('.user-agreement-wrap label .checkbox[type=checkbox]+i')
        input.click()
        time.sleep(3)
        input = browser.find_element_by_name('commit')
        input.click()
        time.sleep(10)

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

def try_mt():
    url = 'https://passport.meituan.com/account/unitivelogin'
    # user = input('user: ')
    # password = input('password: ')
    user = '13950885962'
    password = 'tong654321tong'
    spider = page_spider(url, user, password)
    spider.get_cookies()


if __name__ == '__main__':
    # main()
    try_mt()
