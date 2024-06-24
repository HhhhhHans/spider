import scrapy
from faker import Faker


class Test(scrapy.Spider):
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'cookie': '__utmv=30149280.25245;__utmc=223695111;__utmz=30149280.1717143242.31.9.utmcsr=bing|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided);_pk_id.100001.4cf6=03b05e3cf82e6881.1715161706.;bid=gf9tYkQwmvA;ck=YJne;__utmb=223695111.0.10.1717402314;__utma=30149280.1501196892.1715160078.1717143242.1717402307.32;_pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1717402314%2C%22https%3A%2F%2Fwww.douban.com%2F%22%5D;__utmb=30149280.2.10.1717402307;__utmc=30149280;_vwo_uuid_v2=D627A3199C760393908F906371366342F|c54424e711adb0cff2ed710569e47165;__utma=223695111.1029353850.1715161706.1717143250.1717402314.27;__utmt=1;__utmz=223695111.1717402314.27.16.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/;_ga=GA1.2.1501196892.1715160078;_ga_PRH9EWN86K=GS1.2.1715593787.1.0.1715593787.0.0.0;_pk_ses.100001.4cf6=1;ap_v=0,6.0;ct=y;dbcl2="252450422:OGgPrxA7Jjs";douban-fav-remind=1;Hm_lvt_19fc7b106453f97b6a84d64302f21a04=1715593786;ll="118220";push_doumail_num=0;push_noty_num=0',
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

    name = 'test'  # 爬虫名称
    allowed_domains = ['douban.com']  # 爬虫域

    def start_requests(self):
        yield scrapy.Request(
            url='https://www.douban.com/people/148653196/statuses?p=1',
            headers=self.headers,
            callback=self.test_parse)

    def test_parse(self, response):
        if not response.body:
            print("nonono")
        else:
            print(response.xpath())
        return
