import json
from typing import Optional, Any
from ScrapyDemo.items import UserItem
import scrapy
from faker import Faker


class User(scrapy.Spider):
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'cookie': '__utmv=30149280.25245;__utmz=30149280.1717143242.31.9.utmcsr=bing|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided);bid=gf9tYkQwmvA;_pk_id.100001.8cb4=83725545b41f30ce.1715160078.;_pk_ref.100001.8cb4=%5B%22%22%2C%22%22%2C1719024104%2C%22https%3A%2F%2Fwww.bing.com%2F%22%5D;ck=IFzB;_pk_ses.100001.8cb4=1;__utma=30149280.1501196892.1715160078.1717845853.1719024105.41;__utmb=30149280.3.10.1719024105;__utmc=30149280;__utmt=1;_ga=GA1.2.1501196892.1715160078;_ga_PRH9EWN86K=GS1.2.1715593787.1.0.1715593787.0.0.0;ap_v=0,6.0;dbcl2="252450422:DErQoa6etW4";douban-fav-remind=1;Hm_lvt_19fc7b106453f97b6a84d64302f21a04=1715593786;ll="118220";push_doumail_num=0;push_noty_num=0',
        'Host': 'www.douban.com',
        'Sec-Ch-Ua': '"Chromium";v="124", "Microsoft Edge";v="124", "Not-A.Brand";v="99"',
        'Sec-Ch-Ua-Mobile': '?0',
        'Sec-Ch-Ua-Platform': '"Windows"',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0',
    }

    name = 'user'  # 爬虫名称
    allowed_domains = ['douban.com']  # 爬虫域
    count = 0
    data = {}
    p = 1
    data_index = 0
    start_ulrs = []
    movie = {}
    comment = {}
    current_like = []


    def __init__(self, name: Optional[str] = None, category: Optional[str] = None, **kwargs: Any):
        super().__init__(name, **kwargs)
        with open('data\\out7.json', 'r', encoding='utf-8') as file:
            self.p = 1
            self.data_index = 0
            self.data = json.load(file)
            self.movie = self.data[self.data_index]
            self.comment = self.movie['comment_url'].popitem()
            self.start_urls = [self.comment[0] + "statuses?p=%s" % self.p]

    def start_requests(self):
        yield scrapy.Request(
            url=self.start_urls[0],
            headers=self.headers,
            callback=self.like_parse,dont_filter=True)

    def like_parse(self, response):
        judge = response.xpath("//div[@class='new-status status-wrapper    ']")
        if len(judge) != 0:
            titles = response.xpath("//div[contains(@class, 'new-status status-wrapper') and .//div[contains(@class, 'text') and contains(., '看过')] and .//span[contains(@class, 'rating-stars') and (contains(text(), '★★★★☆') or contains(text(), '★★★★★'))]]//div[@class='title']/a/text()")
            for title in titles:
                name = str(title).split(' ')[0]
                self.current_like.append(name)
            if len(self.current_like) <= 4:
                self.p += 1
                yield scrapy.Request(url=self.comment[0] + "statuses?p=%s" % self.p,
                                     headers=self.headers,
                                     callback=self.like_parse,dont_filter=True)
                return
        item = UserItem()
        item['name'] = self.movie['name']
        item['comment'] = self.comment[1]
        item['like'] = self.current_like
        yield item
        self.current_like = []
        if len(self.movie['comment_url']) == 0:
            self.data_index += 1
            if self.data_index >= len(self.data):
                return
            self.movie = self.data[self.data_index]
        self.comment = self.movie['comment_url'].popitem()
        self.p = 1
        yield scrapy.Request(url=self.comment[0] + "statuses?p=%s" % self.p,
                              headers=self.headers,
                              callback=self.like_parse,dont_filter=True)

