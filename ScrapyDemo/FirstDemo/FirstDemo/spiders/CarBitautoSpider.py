import scrapy
import re
import hashlib
import os

class CarBitautoSpider(scrapy.Spider):
    name = 'CarBitautoSpider'
    allowed_domains = ['bitauto.com']
    start_urls = [
        'http://car.bitauto.com/wulingzhiguang/wenzhang/',
        'http://car.bitauto.com/hongguangv/wenzhang/',
        'http://car.bitauto.com/wulingrongguang/wenzhang/',
        'http://car.bitauto.com/zhengcheng/wenzhang/',
        'http://car.bitauto.com/wulingzhiguangv/wenzhang/',
        'http://car.bitauto.com/xiaohaishix30l/wenzhang/',
        'http://car.bitauto.com/changanzhixing3/wenzhang/',
        'http://car.bitauto.com/changanzhixing9/wenzhang/',
        'http://car.bitauto.com/jinbeix30/wenzhang/',
        'http://car.bitauto.com/dongfengxiaokangc36/wenzhang/',
        'http://car.bitauto.com/changankuayuexinnengyuanv5/wenzhang/',
        'http://car.bitauto.com/dongfengc37/wenzhang/',
        'http://car.bitauto.com/letu/wenzhang/',
        'http://car.bitauto.com/dongfengxiaokangk17/wenzhang/',
        'http://car.bitauto.com/kuayuev3/wenzhang/',
        'http://car.bitauto.com/weiwang306/wenzhang/',
        'http://car.bitauto.com/aolingt3/wenzhang/',
        'http://car.bitauto.com/kairuiyouya/wenzhang/',
        'http://car.bitauto.com/changanv5/wenzhang/',
        'http://car.bitauto.com/xiaokangk07s/wenzhang/',
        'http://car.bitauto.com/dongfengxiaokangk07/wenzhang/',
        'http://car.bitauto.com/beiqiweiwang307/wenzhang/',
        'http://car.bitauto.com/xiaokangk05s/wenzhang/',
        'http://car.bitauto.com/junfeng-4069/wenzhang/',
        'http://car.bitauto.com/zhongtaiv10/wenzhang/',
        'http://car.bitauto.com/a7/wenzhang/',
        'http://car.bitauto.com/kairuiyouyou/wenzhang/',
        'http://car.bitauto.com/changankuayuexinnengyuanv3/wenzhang/',
        'http://car.bitauto.com/dongfengxiaokangc35/wenzhang/',
        'http://car.bitauto.com/yiqijiabao/wenzhang/',
        'http://car.bitauto.com/fengjingv5ev/wenzhang/',
        'http://car.bitauto.com/dongfengxiaokangk07-3258/wenzhang/',
        'http://car.bitauto.com/dongfengxiaokangv29/wenzhang/',
        'http://car.bitauto.com/m70evxiangshiyunshuche2zuoban/wenzhang/',
        'http://car.bitauto.com/jinbeihaishix30lev/wenzhang/',
        'http://car.bitauto.com/dongfengxiaokangv70s/wenzhang/',
        'http://car.bitauto.com/a9/wenzhang/',
        'http://car.bitauto.com/jiabaov52/wenzhang/',
        'http://car.bitauto.com/v75/wenzhang/',
        'http://car.bitauto.com/v77/wenzhang/',
        'http://car.bitauto.com/qitengm70/wenzhang/',
        'http://car.bitauto.com/fengshun/wenzhang/'
    ]

    def parse(self, response):
        for url in response.css('div.inner-box div.details h2 a::attr(href)').getall():
            print('article url: %s' % url)
            yield scrapy.Request(url, callback=self.parse_article)

    def parse_article(self, response):
        url = response.url

        title = response.css('h1.tit-h1::text').get()
        content = response.xpath('//div[@id="openimg_articlecontent"]//text()').getall()
        text = ' '.join(content)
        text += title
        text = re.sub(r'\s', ' ', text)

        urlMd5 = hashlib.md5(url.encode('utf-8')).hexdigest()
        path = 'E:\\test\\cheliangfuwu\\%s' % self.name
        isExists = os.path.exists(path)
        if not isExists:
            os.makedirs(path)
        filename = 'E:\\test\\cheliangfuwu\\%s\\%s' % (self.name, urlMd5)
        if len(text) > 10:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(text)
        else:
            print('text is too short, url: %s' % url)