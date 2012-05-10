from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request
import urllib
import codecs
import unicodedata

class LyricsSpider(BaseSpider):
    name = "lyrics"
    allowed_domains = ["cowboylyrics.com"]
    base_url = "http://www.cowboylyrics.com/lyrics/"
    start_urls = [base_url+"lambert-miranda.html"]
    dir_name = 'corpus/'
    
    def parse(self, response):
        
        hxs = HtmlXPathSelector(response)
        urls = hxs.select('//li/a/@href').extract()
        for song_url in urls:
            song_url = self.base_url+song_url
            print song_url
            request = Request(song_url, callback=self.parseLyricsPage)
            yield request

    def parseLyricsPage(self, response):
       hxs = HtmlXPathSelector(response)
       title = hxs.select('//title/text()').extract()[0]
       filename = self.dir_name + title+'.txt'
       f = codecs.open(filename, encoding='utf-8', mode='w')
       lines = hxs.select('//br').extract()
       for line in lines:
           if line.find('\n') != -1:
               text = line.split('\n')[-1]
               text = unicodedata.normalize('NFKD', text)
               if not text.isspace():
                   f.write(text + '\n')
       f.close() 
           

