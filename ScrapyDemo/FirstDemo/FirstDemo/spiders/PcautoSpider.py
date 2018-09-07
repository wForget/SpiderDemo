import scrapy
import re
import os
import hashlib

class PcautoSpider(scrapy.Spider):
    name = 'PcautoSpider'
    allowed_domains = ['pcauto.com.cn']
    start_urls = [
        'http://price.pcauto.com.cn/top/k105-p1.html',
        'http://price.pcauto.com.cn/top/k105-p2.html',
        'http://price.pcauto.com.cn/top/k105-p3.html',
        'http://price.pcauto.com.cn/top/k105-p4.html',
    ]

    def parse(self, response):
        for url in response.css('p.sname a::attr(href)').getall():
            url = 'http://price.pcauto.com.cn%sarticle.html' % url
            print('list url: %s' % url)
            yield scrapy.Request(url, callback=self.parse_list)

    def parse_list(self, response):
        for url in list(set(response.css('div.topico a::attr(href)').getall())):
            url = 'http:%s' % url
            print('article url: %s' % url)
            yield scrapy.Request(url, callback=self.parse_article)

    def parse_article(self, response):
        url = response.url

        title = response.css('h1.artTit span.tit::text').get()
        if title is None or len(title) == 0:
            title = response.css('h1.artTit::text').get()
        content = response.xpath('//div[@class="artText clearfix"]//text()').getall()
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