import scrapy

class FixpriceSpider(scrapy.Spider):
    name = 'fixprice_for_home'
    start_urls = ['https://fix-price.com/catalog/dlya-doma']

    def parse(self, response):
        product_page_links = response.css('.products .information a::attr(href)').getall()
        yield from response.follow_all(product_page_links, callback=self.parse_product)

        pagination_links = response.css('.pages.is-adaptive a')[-1]
        yield response.follow(pagination_links, self.parse)

    def parse_product(self, response):
        price = response.css('div.price::text').get().split()[0]
        if ',' in price:
            price = price.replace(',', '.')
        yield {'Название': response.css('h1.title::text').get(),
               'Цена': float(price),
               'Ссылка': response.url,
                }
