import requests
from bs4 import BeautifulSoup

head = {  # 模拟浏览器头部信息，向服务器发送消息
    "User-Agent": "Mozilla / 5.0(Windows NT 10.0;Win64;x64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 83.0.4103.116Safari / 537.36"
}  #

def get_one_page(url):
