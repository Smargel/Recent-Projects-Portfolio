import scrapy
from reuters.items import ReutersItem
from datetime import datetime
import re


class Reuters(scrapy.Spider):
    name = "reuters_scraper"

    # First Start Url
    start_urls = ["https://www.reuters.com/news/archive/technologynews?view=page&page=1&pageSize=10"]

    npages = 100

    # This mimics getting the pages using the "earlier" button
    for i in range(2, npages + 2):
        start_urls.append("https://www.reuters.com/news/archive/technologynews?view=page&page="+str(i)+"&pageSize=10"+"")

    def parse(self, response):
        for href in response.xpath("//div[@class='story-content']//a/@href"):
            # add the scheme, eg http://
            url  = "https://www.reuters.com/article" + href.extract()            
            yield scrapy.Request(url, callback=self.parse_dir_contents)

    def parse_dir_contents(self, response):
        item = ReutersItem()

        # Getting the title of the article
        item['title'] = response.xpath("//h1[contains(@class, 'ArticleHeader_headline')]/descendant::text()").extract()[0].strip()

        # Getting the pull quote
        item['summary']= response.xpath("//div[contains(@class, 'StandardArticleBody_body')]//p/descendant::text()").extract()[0]

        # Getting the journalist who wrote the piece
        item['author'] = response.xpath("//div[contains(@class, 'BylineBar_byline')]//span//a[starts-with(@href, '/journalists/')]/text()").extract()

        item['datePublished'] = response.xpath("//div[contains(@class, 'ArticleHeader_date') and substring-before(., '/')]/text()").extract()

        yield item 