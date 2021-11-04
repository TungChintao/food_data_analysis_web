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
from pyasn1.compat.octets import null
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

ALLCITIES = ['北京', '上海', '广州', '天津', '重庆',
             '深圳', '石家庄', '太原', '呼和浩特', '沈阳',
             '长春', '哈尔滨', '南京', '杭州', '合肥', '福州', '厦门',
             '南昌', '济南', '郑州', '武汉', '长沙','南宁', '海口','成都', '贵阳', '昆明', '拉萨',
             '西安','兰州', '西宁', '银川', '乌鲁木齐', '苏州', '三亚']

KEYWORD = '奶茶'
PATH = './data/'
MAX_PAGE_INDEX = 1


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
        self.headers = self.get_ua()  # {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, '
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
            # 'https': 'https://' + proxy,
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
        # sx = pinyin(self.name, style=Style.FIRST_LETTER)
        # name = ''.join(item[0] for item in sx)
        # link = 'https:' + '//' + name + '.meituan.com/s/' + self.keyword
        # return link
        response = rq.get('http://www.meituan.com/changecity', headers=self.headers)
        soup = BeautifulSoup(response.text, 'lxml')
        cities = soup.find_all('a', {'class': 'link city'})
        # print(cities)
        for c in cities:
            print(c.text)
            if self.name in c.text or c.text in self.name:
                link = 'https:' + c.attrs['href'] + '/s/' + self.keyword
                return link

    def get_city_id(self):
        headers = dict(self.headers, Cookie=self.cookie, Host=self.host)
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
        cookies = [
            #'uuid=acd029b79a9c4f55bd83.1635852089.1.0.0; _lxsdk_cuid=17ce061fff6c8-0e49a6c8d64e54-57b193e-144000-17ce061fff6c8; mtcdn=K; userTicket=oidSBzbiroKGSBHRCGITfRLNoXSSNTjMrQmdewEC; u=932521003; n=FJl205508568; lt=l5EegJfTNCSKniAYGiXQmOEwGR0AAAAAAw8AAPQgUNVSrQ6xBnXzrsqMktN6LxIXLMG9luuDDGIjqYjucQUEwq8UAQn-oaCbOmc24Q; mt_c_token=l5EegJfTNCSKniAYGiXQmOEwGR0AAAAAAw8AAPQgUNVSrQ6xBnXzrsqMktN6LxIXLMG9luuDDGIjqYjucQUEwq8UAQn-oaCbOmc24Q; token=l5EegJfTNCSKniAYGiXQmOEwGR0AAAAAAw8AAPQgUNVSrQ6xBnXzrsqMktN6LxIXLMG9luuDDGIjqYjucQUEwq8UAQn-oaCbOmc24Q; lsu=; _lx_utm=utm_source=Baidu&utm_medium=organic; firstTime=1635852189814; unc=FJl205508568; _lxsdk_s=17ce061fff7-c88-e2-2f8||17',
            '__mta=45988635.1635851985784.1635851985784.1635851985784.1; uuid=06c2130674334a9d988a.1635851920.1.0.0; _lxsdk_cuid=17ce05f6684c8-00a6d06438b9d-a7d173c-1fa400-17ce05f6684c8; mtcdn=K; userTicket=MxdHPpZdxduPGMzsoFQYWxNDXzJHAlzicNrcxqvn; u=3037214466; n=Rtf382032875; lt=lAjkZcM7ooMr-VCtr7zt2yKjyvwAAAAAAw8AAAuIxAqJIkKya-jd0vi6FzNPfBPU_GM910PRzPJ_VS59Xr7DuJPURgI_L1iYlIo_Jg; mt_c_token=lAjkZcM7ooMr-VCtr7zt2yKjyvwAAAAAAw8AAAuIxAqJIkKya-jd0vi6FzNPfBPU_GM910PRzPJ_VS59Xr7DuJPURgI_L1iYlIo_Jg; token=lAjkZcM7ooMr-VCtr7zt2yKjyvwAAAAAAw8AAAuIxAqJIkKya-jd0vi6FzNPfBPU_GM910PRzPJ_VS59Xr7DuJPURgI_L1iYlIo_Jg; lsu=; token2=lAjkZcM7ooMr-VCtr7zt2yKjyvwAAAAAAw8AAAuIxAqJIkKya-jd0vi6FzNPfBPU_GM910PRzPJ_VS59Xr7DuJPURgI_L1iYlIo_Jg; unc=Rtf382032875; ci=1; rvct=1; firstTime=1635851985164; _lxsdk_s=17ce05f6685-ec8-56-2e8||10',
            'uuid=a57ef8fe20a4480497bc.1635851695.1.0.0; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; _lxsdk_cuid=17ce05bf62d81-0a101e728132aa-57b1a33-144000-17ce05bf62ec8; mtcdn=K; lt=uvUWx4K4eb3sPOG1wTXPcp-YQ7QAAAAAAw8AAB9MzgStd2Jezjp1j-nMczeYqhGDg61D_IAyeTkZfQofKIw-OGSbEe55XBf58O7KAA; u=1698635415; n=SyW122693208; token2=uvUWx4K4eb3sPOG1wTXPcp-YQ7QAAAAAAw8AAB9MzgStd2Jezjp1j-nMczeYqhGDg61D_IAyeTkZfQofKIw-OGSbEe55XBf58O7KAA; firstTime=1635851729660; unc=SyW122693208; __mta=119831351.1635851695720.1635851695720.1635851729679.2; _lxsdk_s=17ce05bf62f-e06-59b-a93%7C%7C4',
            'uuid=d1c60ad37df04bf8881e.1635849747.1.0.0; _lx_utm=utm_source=bing&utm_medium=organic; _lxsdk_cuid=17ce03e443cc8-062237b7695632-57b193e-144000-17ce03e443dc8; mtcdn=K; userTicket=ZWteExbxhMAGnNMAIotHxnmDUxTcUybZkUFrtxxu; u=3274467902; n=Xri313937237; lt=DRsrzliA3Yjvmk4-wcaNf10iQTcAAAAAAw8AAJCXmwoNcrE24g18Y8ZEPUTExrFpWzDRdsWevHyzpnwvGq97MBa7enc3Czh4qU8tmA; mt_c_token=DRsrzliA3Yjvmk4-wcaNf10iQTcAAAAAAw8AAJCXmwoNcrE24g18Y8ZEPUTExrFpWzDRdsWevHyzpnwvGq97MBa7enc3Czh4qU8tmA; token=DRsrzliA3Yjvmk4-wcaNf10iQTcAAAAAAw8AAJCXmwoNcrE24g18Y8ZEPUTExrFpWzDRdsWevHyzpnwvGq97MBa7enc3Czh4qU8tmA; lsu=; token2=DRsrzliA3Yjvmk4-wcaNf10iQTcAAAAAAw8AAJCXmwoNcrE24g18Y8ZEPUTExrFpWzDRdsWevHyzpnwvGq97MBa7enc3Czh4qU8tmA; firstTime=1635849801028; unc=Xri313937237; _lxsdk_s=17ce03e443e-0a3-973-d99||5',
            #'_lxsdk_cuid=17cdac333f1a2-0e998a61694af5-771103d-144000-17cdac333f2c8; mtcdn=K; _hc.v=95acdf04-95e5-e781-c21e-f65119fdbab2.1635758178; lsu=; ci=44; rvct=44%2C1; uuid=6424caf25c41408e888a.1635774557.1.0.0; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; lat=26.018351; lng=119.218431; _lxsdk=17cdac333f1a2-0e998a61694af5-771103d-144000-17cdac333f2c8; userTicket=DRdOCqrxFaOwCtOwCbjEqoQrbZKEmhWAfkWKvPpU; u=2674332799; n=qjF368475661; lt=S5Nfx9COfohWa2Ok7qcFsJoeyNYAAAAAAw8AAGk_WXuKZUnVbcq7gsAmT8sigtNA3qnijlXDKzbab7TivCq1uRDJqMIk7fNPWVbvWg; mt_c_token=S5Nfx9COfohWa2Ok7qcFsJoeyNYAAAAAAw8AAGk_WXuKZUnVbcq7gsAmT8sigtNA3qnijlXDKzbab7TivCq1uRDJqMIk7fNPWVbvWg; token=S5Nfx9COfohWa2Ok7qcFsJoeyNYAAAAAAw8AAGk_WXuKZUnVbcq7gsAmT8sigtNA3qnijlXDKzbab7TivCq1uRDJqMIk7fNPWVbvWg; token2=S5Nfx9COfohWa2Ok7qcFsJoeyNYAAAAAAw8AAGk_WXuKZUnVbcq7gsAmT8sigtNA3qnijlXDKzbab7TivCq1uRDJqMIk7fNPWVbvWg; firstTime=1635849526622; unc=qjF368475661; __mta=46587672.1635758074474.1635849492210.1635849527908.4; _lxsdk_s=17ce03a45bb-699-8ac-6f4%7C%7C4',
        ]
        return random.choice(cookies)

    def change_cookie(self):
        self.cookie = self.get_cookies()

    def get_userid(self):
        findUserid = re.compile(r'; u=(.*?);', re.S)

        userid = re.search(findUserid, self.cookie).group(1)
        return userid

    def get_uuid(self):
        findUuid = re.compile(r'uuid=(.*?);', re.S)

        uuid = re.search(findUuid, self.cookie).group(1)
        return uuid

    def get_token(self):
        findToken = re.compile(r'token2=(.*?);', re.S)
        token = re.search(findToken, self.cookie).group(1)
        return token

    def get_json(self, page):
        time.sleep(2)
        url = 'https://apimobile.meituan.com/group/v4/poi/pcsearch/{}'
        url += '?uuid={}&userid={}&limit=32&offset={}&cateId=-1&q={}&token={}'
        url = url.format(self.cityid, self.uuid, self.userid, page * 32, self.keyword, self.token)  # API URL

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
        max_page = data['data']['totalCount'] // 32 + 1
        # print(data['data']['totalCount'], MAX_PAGE_INDEX)
        return data['data']['searchResult'], max_page

    def parse_data(self, data, dbManager):
        '''Parse data of one page'''

        for i in range(len(data)):
            temp_shop = {'shop_id': data[i]['id'],
                         'city': self.name}

            fields = ['title', 'backCateName', 'areaname',
                      'latitude', 'longitude', 'avgprice', 'avgscore',
                      'comments', 'historyCouponCount']
            for key in fields:
                temp_shop[key] = data[i][key]
            print(temp_shop)

            dbManager.trans_to_shopdata(temp_shop)

            names = ['title', 'price', 'value']

            goods = data[i]['deals']
            if goods is None:
                continue
            for j in range(len(goods)):
                good = {'shop_id': data[i]['id']}
                for key in names:
                    good[key] = goods[j][key]
                print(good)
                dbManager.trans_to_gooddata(good)


def main():
    dbManager = DataManager('milktea_data')
    for city in ALLCITIES:
        spider = MtSpider(city, KEYWORD)
        spider.change_cookie()
        page = 0
        max_page = 1
        while page < max_page:
            try:
                data, max_page = spider.get_json(page)
                # print(data)
                spider.parse_data(data, dbManager)
                print('>>> Page No.%d finished...' % (page + 1))
            except Exception as e:
                print('Spider Error: ', e)
                spider.change_parm()
                spider.change_cookie()
                continue
            page += 1
            spider.change_parm()
            time.sleep(5)
            # trans_to_mysql(data, 'milktea_data')
    dbManager.close_db()


if __name__ == '__main__':
    main()
