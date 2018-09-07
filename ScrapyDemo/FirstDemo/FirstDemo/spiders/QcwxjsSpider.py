import scrapy
import hashlib
import re

'''
http://www.qcwxjs.com
'''
class QcwxjsSpider(scrapy.Spider):
    name = 'QcwxjsSpider'
    allowed_domains = ['www.qcwxjs.com']
    start_urls = ['http://www.qcwxjs.com/']

    def parse(self, response):
        for url in list(set(response.xpath('//a/@href').re(r'.*www.qcwxjs.com/sort.*'))):
            #print('sort url: %s' % url)
            yield scrapy.Request(url, callback=self.parse_list)

    def parse_list(self, response):
        refer = response.url
        #print('refer url: %s' % refer)

        if 'page' not in refer:
            # print(response.css('div#pagenavi a:last-child::attr(href)').get())
            # last_page = int(response.css('div#pagenavi a:last-child::attr(href)').get().split('/')[-1])
            for page in range(2, 10):
                page_url = '%s/page/%s'%(refer, page)
                #print('page url: %s' % page_url)
                yield scrapy.Request(page_url, callback=self.parse_list)


        for url in list(set(response.css('div.loop div.thumb a::attr(href)').re(r'.*www.qcwxjs.com.*'))):
            #print('article url: %s' % url)
            yield scrapy.Request(url, callback=self.parse_article)


    def parse_article(self, response):
        url = response.url
        title = response.css('h1.entry-title::text').get()
        content = response.xpath('//*[@id="main-post"]/div[6]/div[2]//text()').getall()

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

