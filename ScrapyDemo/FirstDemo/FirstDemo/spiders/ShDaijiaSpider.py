import scrapy
import re
import hashlib

class ShDaijiaSpider(scrapy.Spider):
    name = 'ShDaijiaSpider'
    allowed_domains = ['www.sh-daijia.com']
    start_urls = ['http://www.sh-daijia.com/catalog.asp?cate=24']

    def parse(self, response):
        url = response.url
        if url in self.start_urls:
            for i in range(2,7):
                yield scrapy.Request('http://www.sh-daijia.com/catalog.asp?cate=24&page=%s' % i, callback=self.parse)
        for url in list(set(response.css('h2.post-title a::attr(href)').re(r'.*http://www.sh-daijia.com/INFO/.*'))):
            print('article url: %s' % url)
            yield scrapy.Request(url, callback=self.parse_article)

    def parse_article(self, response):
        url = response.url
        title = response.css('h2.post-title::text').get()
        content = response.xpath('//*[@id="divMain"]/div[1]/div/p[position()<(last()-1)]//text()').getall()
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