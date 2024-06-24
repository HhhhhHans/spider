import numpy as np
from lxml import html
import scrapy
from faker import Faker
import re
import json
from ..items import MovieItem
import copy


class Movie_comment(scrapy.Spider):
    name = 'douban'  # 爬虫名称
    allowed_domains = ['douban.com']  # 爬虫域

    # 反爬尝试时写的函数，但最终爬取时没有用到
    '''def get_cookie(self):
        cookie_str = "rpdid=|(m)l)JlY)k0J'u~|J)lYJJu;PVID=1;i-wanna-go-back=-1;buvid4=AC282591-C2BB-7AA9-5358-3B5D08420B1289101-022012710-mz92sA0MD%2FXLzgnCN2s0%2Fg%3D%3D;bp_video_offset_227405475=924940757889974274;CURRENT_BLACKGAP=0;b_lsid=B8BC102104_18F764A0FAA;b_lsid=7AC7E1C8_18F7674C714;home_feed_column=4;hit-dyn-v2=1;sid=g27zfdfd;bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MTU4Mjk3OTksImlhdCI6MTcxNTU3MDUzOSwicGx0IjotMX0.PDoLPfe_DOGnxMyDeg48xBf599PtCJlFFeskZ3Q7ESw;home_feed_column=4;buvid4=DD2AECEF-58C3-3E44-CC81-DD9E66346FEA16158-024051409-LtMUHU%2FsvLkOtBhBfWxo0A%3D%3D;CURRENT_FNVAL=4048;b_ut=5;header_theme_version=CLOSE;buvid3=91F42376-9EDC-FF30-3101-3ACC88C6723815329infoc;bili_jct=5d431377cf506c958dabd73019f79512;sid=fmgc0zlm;buvid_fp_plain=undefined;LIVE_BUVID=AUTO8516270412869609;bp_t_offset_227405475=931300964518854663;SESSDATA=a9275b88%2C1731231376%2C94650%2A51CjBC4qbq2AypagLMjf3nmtUiqxE1Mo6mZSgd6hZPaAhL-4Gj5NEVgCPRHT1XBmhq0pwSVllmVThsb3RyR1Bpa2w5NVZiSzl2VGItOFpEaUo4cExRaTU4Q3VRVVhtTzVxRlFaNTlIOFNXWlVVRTVUZ0NhYWRFZWNTX2F4YU5WeTFBdW1ycGpoUk9RIIEC;enable_web_push=DISABLE;bsource=share_source_qqchat;CURRENT_QUALITY=80;bmg_src_def_domain=i2.hdslb.com;b_nut=100;b_nut=1715679315;_uuid=DF312ACD-8974-10652-BD2D-7E3C1049F122B15743infoc;_uuid=BB96B957-F91C-6C7E-43AD-CBC735E5EC3133462infoc;bili_jct=d49d1cd6892f111f86a6f4f0e7324773;bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MTU5Mzg1MTYsImlhdCI6MTcxNTY3OTI1NiwicGx0IjotMX0.qYnSng-tokXmaPoMiOvvNsVha4QN577N3ivmtpiPWUE;bili_ticket_expires=1715938456;bili_ticket_expires=1715829739;bmg_af_switch=1;bp_t_offset_227405475=931324737167032324;browser_resolution=820-449;browser_resolution=1368-781;bsource=share_source_qqchat;buvid3=FD6DA737-22FD-468C-8109-B5A45F472A5434779infoc;buvid_fp=315395266ce2f77926307cfe0ab346c5;buvid_fp=315395266ce2f77926307cfe0ab346c5;DedeUserID=227405475;DedeUserID=227405475;DedeUserID__ckMd5=0ef9cfc4e61faa45;DedeUserID__ckMd5=0ef9cfc4e61faa45;enable_web_push=DISABLE;FEED_LIVE_VERSION=V8;fingerprint=3a51a15f3cc418f2ea3859d6a3754ed0;header_theme_version=CLOSE;hit-dyn-v2=1;hit-new-style-dyn=1;PVID=4;SESSDATA=c1cb6952%2C1731122597%2C0ac1e%2A52CjDIIHea2bp3BFqNYeReZAK9vfqAHejal4CKgt45dSEghkGaQOHx1tvLL__uzo3y8fsSVm1YY2dZNC1tWHpaMk5Qd0c1WDI5LXg1TkUtSVVrQTE3bWtaWkdxbk51a3VOLW5MZTU4U2RJQ0pIQ09vR19uNHVZbG1JT1IzMVJlR3hyVHVMSWI1RFVnIIEC;share_source_origin=QQ"
        cookie = {}
        cookie_split = cookie_str.split(';')
        for line in cookie_split:
            key, value = line.split('=', 1)
            cookie[key] = value
        return cookie

    def get_json(self):
        with open('../cookie.json', 'r') as f:
            cookies_json = json.load(f)
        return cookies_json'''

    def start_requests(self):
        ua = Faker()
        headers = {
            "user-agent": ua.chrome(is_pc=True),
        }
        movie_id = np.loadtxt('movie_id.out', dtype='i').tolist()
        for i in range(250):
            mid = movie_id[i]
            yield scrapy.Request(
                url='https://movie.douban.com/subject/%s/comments?start=0&limit=100&status=P&sort=new_score' % mid,
                headers=headers,
                callback=self.movie_parse)

    def movie_parse(self, response):
        name = response.xpath('//div[@id="content"]/h1/text()').extract()[0].split(' ')[0]
        comment_table = response.xpath('//div[@class="comment-item "]')
        comment_url = {}
        rating = comment_table.xpath('//span[starts-with(@class, "allstar") and contains(@class, "rating")]')
        comment = comment_table.xpath('//span[@class="short"]/text()').extract()
        people_url = comment_table.xpath('//span[@class="comment-info"]/a/@href').extract()
        for i in range(100):
            temp = rating[i]
            rating_value = temp.xpath('@class').get()
            match = re.search(r'allstar(\d+) rating', rating_value)
            number = match.group(1)
            comment_url[str(comment[i])] = number
            # comment_url[str(people_url[i])] = str(comment[i])
        item = MovieItem()
        item['name'] = name
        item['comment_url'] = comment_url
        yield item
