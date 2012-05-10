from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
import urllib
import codecs
import unicodedata

class LyricsSpider(BaseSpider):
    name = "lyrics"
    allowed_domains = ["cowboylyrics.com"]
    start_urls = ["http://www.cowboylyrics.com/lyrics/swift-taylor/mine-30826.html"]

    def parse(self, response):
       hxs = HtmlXPathSelector(response)
       title = hxs.select('//title/text()').extract()[0]
       filename = title+'.txt'
       f = codecs.open(filename, encoding='utf-8', mode='w')
       sites = hxs.select('//br')
       rootpath = "./";
       for site in sites:
           line = site.extract()
           if line.find('\n') != -1:
               text = line.split('\n')[-1]
               text = unicodedata.normalize('NFKD', text)
               if not text.isspace():
                   f.write(text + '\n')
       f.close() 
           

