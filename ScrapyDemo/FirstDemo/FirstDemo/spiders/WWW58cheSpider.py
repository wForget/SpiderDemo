import scrapy
import re
import hashlib
import os

class WWW58cheSpider(scrapy.Spider):
    name = 'WWW58cheSpider'
    allowed_domains = ['58che.com']
    start_urls = ['http://www.58che.com/']

    def parse(self, response):
        for url in response.css('div#iconav ul li>a::attr(href)').getall():
            #print('url: http:%s' % url)
            url = 'http:%s' % url
            yield scrapy.Request(url, callback=self.parse_one)

    def parse_one(self, response):
        type = get_refer_type(response.url)
        for url in list(set(response.css('div#l_onDiv div.in_wt_nr ul li dl dt a::attr(href)').getall())):
            #print('url: http:%sarticle.html' % url)
            url = 'http:%sarticle.html?type=%s' % (url, type)
            yield scrapy.Request(url, callback=self.parse_two, meta={'type' : type})

    def parse_two(self, response):
        for url in response.css('div.artinfo div.content a::attr(href)').getall():
            #print('article url: http:%s' % url)
            url = 'http:%s' % url
            yield scrapy.Request(url, callback=self.parse_article, meta=response.meta)

    def parse_article(self, response):
        url = response.url
        type = response.meta.get('type')
        if type is None:
            print('type is None, url:' + url)
            return

        title = response.css('h1.h_title::text').get()
        content = response.xpath('//div[@class="c_tcon clearfix"]//text()').getall()
        text = ' '.join(content)
        text += title
        text = re.sub(r'\s', ' ', text)

        urlMd5 = hashlib.md5(url.encode('utf-8')).hexdigest()
        path = 'E:\\test\\cheliangfuwu\\%s\\%s' % (self.name, type)
        isExists = os.path.exists(path)
        if not isExists:
            os.makedirs(path)
        filename = 'E:\\test\\cheliangfuwu\\%s\\%s\\%s' % (self.name, type, urlMd5)
        if len(text) > 10:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(text)
        else:
            print('text is too short, url: %s' % url)

def get_refer_type(refer_url):
    return refer_url.split('/')[-2]