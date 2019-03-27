import scrapy
from scrapy import Request
from doubanSpider.items import DoubanBookItem

class doubanSpider(scrapy.Spider):
    name = "douban_top250_book"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
    }
    rank = 0

    def start_requests(self):
        url = 'https://book.douban.com/top250'
        yield Request(url, headers=self.headers)

    def parse(self, response):
        item = DoubanBookItem()
        books = response.xpath('//div[@class="indent"]//tr[@class="item"]')

        for book in books:
            self.rank += 1
            # 没有在网页中找到排名，手动计数
            item['ranking'] = self.rank
            item['book_name'] = book.xpath('.//div[@class="pl2"]/a/@title').extract_first()
            item['score'] = book.xpath('.//span[@class="rating_nums"]/text()').extract_first()
            item['score_num'] = book.xpath('.//div[@class="star clearfix"]/span[@class="pl"]/text()').re_first('(\d+)人评价')
            item['des'] = book.xpath('.//p[@class="quote"]/span/text()').extract_first()
            yield item

        next_url = response.xpath('//span[@class="next"]/a/@href').extract_first()
        if next_url:
            yield Request(next_url, headers=self.headers)

