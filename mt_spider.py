import re
import time
import json
import random
import urllib
import http.cookiejar
import pandas as pd
import requests as rq
from bs4 import BeautifulSoup
from pypinyin import pinyin, Style
from database_execute import DataManager

proxypool_url = 'http://127.0.0.1:5555/random'

user_agents = [
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 OPR/26.0.1656.60',
    'Mozilla/5.0 (Windows NT 5.1; U; en; rv:1.8.1) Gecko/20061208 Firefox/2.0.0 Opera 9.50',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; en) Opera 9.50',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0',
    'Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2 ',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
    'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.16 (KHTML, like Gecko) Chrome/10.0.648.133 Safari/534.16',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)',
    'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 SE 2.X MetaSr 1.0',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; SE 2.X MetaSr 1.0) ',
]

ALLCITIES = ['北京', '上海', '广州', '深圳', '天津', '重庆',
    '石家庄', '太原', '呼和浩特', '沈阳', '长春', '哈尔滨', '南京', '杭州', '合肥',
    '福州', '南昌', '济南', '郑州', '武汉', '长沙', '南宁', '海口', '成都', '贵阳',
    '昆明', '拉萨', '西安', '兰州', '西宁', '银川', '乌鲁木齐']

KEYWORD = '奶茶'
PATH = './data/'


class MtSpider:
    """
    Parameters: cityname[String] | keyword[String]
    Feature: Get n-pages search resutl on meituan, with given keyword and city.
    """

    def __init__(self, cityname, keyword):

        self.proxies = self.get_proxies()

        self.name = cityname
        self.keyword = urllib.parse.quote(keyword)
        # print(self.keyword)
        self.headers = self.get_ua() #{'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, '
                         #             'like Gecko) Chrome/83.0.4103.116 Safari/537.36'}
        self.citylink = self.get_city_link()
        print(self.citylink)
        self.host = self.citylink.split('/')[2]
        print(self.host)
        self.cookie = self.get_cookies()
        print(self.cookie)
        self.uuid = self.get_uuid()
        self.userid = self.get_userid()
        self.token = self.get_token()
        self.cityid = self.get_city_id()
        print(self.cityid)

    def get_random_proxy(self):
        """
        get random proxy from proxypool
        :return: proxy
        """
        return rq.get(proxypool_url).text.strip()

    def get_proxies(self):
        proxy = self.get_random_proxy()
        proxies = {
            'http': 'http://' + proxy,
            #'https': 'https://' + proxy,
        }
        return proxies

    def get_ua(self):
        """
        随机获取 user-agent
        :return:
        """
        user_agent = random.choice(user_agents)
        return {'User-Agent': user_agent}

    def change_parm(self):
        self.proxies = self.get_proxies()
        self.headers = self.get_ua()


    def get_city_link(self):
        """Called during initializing"""

        time.sleep(2)
        sx = pinyin('福州', style=Style.FIRST_LETTER)
        name = ''.join(item[0] for item in sx)
        link = 'https:' + '//'+name+'.meituan.com/s/' + self.keyword
        return link
        # response = rq.get('http://www.meituan.com/changecity', headers=self.headers)
        # soup = BeautifulSoup(response.text, 'lxml')
        # cities = soup.find_all('a', {'class': 'link city'})
        # # print(cities)
        # for c in cities:
        #     print(c.text)
        #     if self.name in c.text or c.text in self.name:
        #         link = 'https:' + c.attrs['href'] + '/s/' + self.keyword
        #         return link

    def get_city_id(self):
        headers = dict(self.headers, Cookie=self.cookie,Host=self.host)
        response = rq.get(self.citylink, headers=headers, proxies=self.proxies)
        id = re.findall(r'{"id":(\d+),"name"', response.text)[0]

        return id

    def get_cookies(self):
        # jar = http.cookiejar.CookieJar()
        # processor = urllib.request.HTTPCookieProcessor(jar)
        # opener = urllib.request.build_opener(processor)
        #
        # _ = opener.open(self.citylink)
        # cookies = []
        # for i in jar:
        #     cookies.append(i.name + '=' + i.value)
        # return ';'.join(cookies)
        return 'your cookie'

    def get_userid(self):
        findUserid = re.compile(r'; u=(.*?);', re.S)

        userid = re.search(findUserid, self.cookie).group(1)
        return userid

    def get_uuid(self):
        findUuid = re.compile(r'uuid=(.*?);', re.S)

        uuid = re.search(findUuid, self.cookie).group(1)
        return uuid

    def get_token(self):
        findToken = re.compile(r'token=(.*?);', re.S)
        token = re.search(findToken, self.cookie).group(1)
        return token

    def get_json(self, page):
        time.sleep(2)
        url = 'https://apimobile.meituan.com/group/v4/poi/pcsearch/{}'
        url += '?uuid={}&userid={}&limit=32&offset={}&cateId=-1&q={}&token={}'
        url = url.format(self.cityid, self.uuid, self.userid, page * 32, self.keyword, self.token)  # API URL
        # url = 'https://apimobile.meituan.com/group/v4/poi/pcsearch/44?uuid=921277537fa24939a49f.1635309002.1.0.0&userid=1046899153&limit=32&offset=0&cateId=-1&q=%E5%A5%B6%E8%8C%B6&token=XSwWfxkTYfrs1BNFkUh7dF3ytf4AAAAACw8AAHaLckJqQnQWXgr-5en7WpyQ0d2GyWx6_1sMZWHw4OOVgXTXKcML_r6VYG1r4BELdg'
        print(url)
        headers = {
            'Host': 'apimobile.meituan.com',
            'Origin': 'https://' + self.host,
            'Referer': self.citylink,
            'User-Agent': self.headers['User-Agent']
        }
        response = rq.get(url, headers=headers, proxies=self.proxies)
        data = json.loads(response.text)
        # print(data)
        return data['data']['searchResult']

    # def parse_data(self, data):
        '''Parse data of one page'''

        # def drop_keys(item, *drops):
        #     copy = item.copy()
        #     [copy.pop(name) for name in drops]
        #     return copy
        # fields = ['id', 'title', 'backCateName', 'areaname',
        #         'latitude', 'longitude', 'avgprice', 'avgscore',
        #         'comments', 'historyCouponCount']
        # drops = list(set(data[0].keys()) - set(fields))
        # shops = pd.DataFrame([drop_keys(d, *drops) for d in data])
        #
        # names = ['drop_id', 'title', 'price', 'value']
        # dicts = []
        #
        # for i in range(len(data)):
        #     if data[i]['deals'] and type(data[i]['deals'][0]) == dict:
        #         for d in data[i]['deals']:
        #             d['drop_id'] = shops.loc[i, 'id']
        #             dicts.append(d)
        #
        # deals = pd.DataFrame(dicts)
        # deals.drop(set(deals.columns) - set(names), axis=1, inplace=True)
        #
        # return deals, shops
    def parse_data(self, data, dbManager):

        for i in range(len(data)):
            temp_shop = {}
            temp_shop['shop_id'] = data[i]['id']
            temp_shop['city'] = self.name

            fields = ['title', 'backCateName', 'areaname',
                    'latitude', 'longitude', 'avgprice', 'avgscore',
                    'comments', 'historyCouponCount', 'deals']
            for key in fields:
                temp_shop[key] = data[i][key]
            print(temp_shop)

            dbManager.trans_to_shopdata(temp_shop)

            names = ['title', 'price', 'value']

            goods = data[i]['deals']

            for i in range(len(goods)):
                good = {}
                good['shop_id'] = data[i]['id']
                for key in names:
                    good[key] = goods[i][key]
                dbManager.trans_to_gooddata(goods)


def main():
    pages = 40
    dbManager = DataManager('milktea_data')
    for city in ALLCITIES:
        spider = MtSpider(city, KEYWORD)
        for page in range(pages):
            try:
                data = spider.get_json(page)
                # print(data)
                spider.parse_data(data, dbManager)
                print('>>> Page No.{page+1} finished...')
            except Exception as e:
                print(e)
                spider.change_parm()
                continue
            spider.change_parm()
            time.sleep(2)
            # trans_to_mysql(data, 'milktea_data')
    dbManager.close_db()


if __name__ == '__main__':
    main()
