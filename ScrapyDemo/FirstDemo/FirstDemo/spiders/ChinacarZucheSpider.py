import scrapy
import re
import hashlib

class ChinacarZucheSpider(scrapy.Spider):
    name = 'ChinacarZucheSpider'
    allowed_domains = ['www.chinacar.com.cn']
    start_urls = ['http://www.chinacar.com.cn/news/news77_1_99_0_0_0_0.html']

    def parse(self, response):
        url = response.url
        if url in self.start_urls:
            for i in range(2,6):
                yield scrapy.Request('http://www.chinacar.com.cn/news/news77_%s_99_0_0_0_0.html' % i, callback=self.parse)
        for url in list(set(response.css('div.tag_lists ul a::attr(href)').re(r'.*newsview.*'))):
            url = 'http://www.chinacar.com.cn' + url
            yield scrapy.Request(url, callback=self.parse_article)

    def parse_article(self, response):
        url = response.url
        title = response.css('article h1::text').get()
        content = response.xpath('//*[@id="content_bit"]/div/article/div[4]//text()').getall()
        text = ' '.join(content)
        text += title
        text = re.sub(r'\s', ' ', text).replace(u'\xa0', u'')

        urlMd5 = hashlib.md5(url.encode('utf-8')).hexdigest()
        filename = 'E:\\test\\cheliangfuwu\\%s\\%s' % (self.name, urlMd5)
        if len(text) > 10:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(text)
        else:
            print('text is too short, url: %s' % url)
