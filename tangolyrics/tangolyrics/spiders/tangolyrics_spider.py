from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request
import urllib
import codecs
import unicodedata
import os

class LyricsSpider(BaseSpider):
    name = "tangolyrics"
    allowed_domains = ["todotango.com"]
    base_subject_url = "http://www.todotango.com/english/biblioteca/letras/"
    base_lyric_url = "http://www.todotango.com/english/las_obras/letra.aspx?idletra="
    start_urls = ["http://www.todotango.com/english/biblioteca/letras/letras.asp"
                  ]
    base_dir_name = 'tangocorpus/'

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        urls = hxs.select('//div[@class="menu"]/a/@href').extract()
        for url in urls:
            # only want the urls in the categories
            if url.startswith('letras'):
                subject_url = self.base_subject_url+url
                request = Request(subject_url, callback=self.parseSubjectPage)
                yield request
                
    def parseSubjectPage(self, response):
        hxs = HtmlXPathSelector(response)
        subject = hxs.select('//title/text()').extract()[0].split('-')[-1].strip()
        dir_name = subject + '/'
        if not os.path.exists(self.base_dir_name+dir_name):
            os.makedirs(self.base_dir_name+dir_name)
        # the url looks like letra.asp?idletra=817
        urls = hxs.select('//div[@class="menu"]/a/@href').extract()
        for url in urls:
            song_url = self.base_lyric_url+url.split('=')[-1]
            #print song_url
            request = Request(song_url, callback=self.parseLyricsPage)
            request.meta['subject'] = subject
            yield request

    def parseLyricsPage(self, response):
       hxs = HtmlXPathSelector(response)
       # title looks like [u'\r\n\tLetra: Al comp\xe1s del coraz\xf3n (Late un coraz\xf3n)\r\n']
       title = hxs.select('//title/text()').extract()[0].split(':')[-1].strip()
       filename = self.base_dir_name + response.meta['subject'] + '/' + title+'.txt'
       print filename
       f = codecs.open(filename, encoding='utf-8', mode='w')
       lines = hxs.select('//span[@id="lbl_Letra"]/text()').extract()
       for line in lines:
           f.write(line + '\n')
       f.close() 
           

