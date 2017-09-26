from scrapy.spiders import Spider
from scrapetest.items import scrapetestItem
from scrapy.http    import Request
import re
 
class MySpider(Spider):
  name = "scrapetest"
  allowed_domains   = []
  start_urls = ["http://code.tutsplus.com/"]
 
  def parse(self, response):
    links = response.xpath('//a/@href').extract()
 
    # We stored already crawled links in this list
    crawledLinks = []
 
    # Pattern to check proper link
    # I only want to get the tutorial posts
    linkPattern = re.compile("^\/tutorials\?page=\d+")
 
    for link in links:
      # If it is a proper link and is not checked yet, yield it to the Spider
      if linkPattern.match(link) and not link in crawledLinks:
        link = "http://code.tutsplus.com" + link
        crawledLinks.append(link)
        yield Request(link, self.parse)
 
    titles = response.xpath('//a[contains(@class, "posts__post-title")]/h1/text()').extract()
    for title in titles:
      item = scrapetestItem()
      item["title"] = title
      yield item
