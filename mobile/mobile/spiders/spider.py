import scrapy
from mobile.items import MobileItem


class MobileSpider(scrapy.Spider):

    name = 'mobile'
    start_urls = ['https://www.whatmobile.com.pk/']

    def parse(self, response):

        urls = response.css("a.lnk::attr(href)").getall()
        samsung_page_url = [
            url for url in urls if "Samsung_Mobiles_Prices" in url]

        absolute_url = response.urljoin(samsung_page_url[0])

        yield response.follow(url=absolute_url, callback=self.samsung_page)

    def samsung_mobiles_page(self, response):

        samsung_mobile_links = response.css(
            "div.mobiles div.item a.BiggerText::attr(href)").extract()
        
        for links in samsung_mobile_links:
            absolute_url = response.urljoin(links)
            yield response.follow(url=absolute_url, callback=self.scrap_mobile_data)

    def scrap_mobile_data(self, response):

        items = MobileItem()

        model_name = response.css("span.Heading1::text").get().strip()

        price = response.css("span.hdng::text").get().strip()

        memory_table = response.css(
            "tr.RowBG2 td.fasla.RowBG1.specs-value.bottom-border::text").getall()
        memory = [memory for memory in memory_table if "RAM" in memory]
        try:
            ram = memory[0].strip().split(',')[1]
            rom = memory[0].strip().split(',')[0]
        except:
            return

        os = response.css(
            "td.fasla.RowBG1.specs-value.bottom-border::text").get().strip()

        items['Model_name'] = model_name
        items['Price'] = price
        items['RAM'] = ram
        items['ROM'] = rom
        items['OS'] = os

        yield items
