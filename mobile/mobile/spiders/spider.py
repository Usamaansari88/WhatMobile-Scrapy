import scrapy

class mobile(scrapy.Spider):

    name='mobilespider'
    start_urls = ['https://www.whatmobile.com.pk/']

    def parse(self, response):

        # title = response.css("title::text").extract()
        # yield{"title":title}
        brands_name = response.css("a.lnk::text")[2:36].extract()
        yield{"Brands":brands_name}
        
        # samsung_page = response.css("a.lnk")[5].attrib['href']
        samsung_page = response.css("a.lnk::attr(href)")[5].get()
        absolute_url = response.urljoin(samsung_page)
        # yield{"Link = ",absolute_url}
        
        yield response.follow(url=absolute_url,callback=self.parse2)
           
    
    def parse2(self, response):
        
        samsung_mobile_links = response.css("div.mobiles div.item a.BiggerText::attr(href)").extract() 
        for links in samsung_mobile_links:
            absolute_url= response.urljoin(links)                    
            yield response.follow(url=absolute_url,callback=self.parse3)          
             
        
    def parse3(self, response):
        
        faulty_mobiles = ['Galaxy Note 7','Galaxy J5 Prime','Galaxy S7 Edge','Galaxy Note 5','Galaxy S7 Edge 128GB','Galaxy S7 Edge','Galaxy C7','Galaxy S8 Plus']              
        
        model_name = response.css("span.Heading1::text").get().strip() 
        if(model_name not in faulty_mobiles):
            price = response.css("span.hdng::text").get().strip()
            ram = response.css("tr.RowBG2 td.fasla.RowBG1.specs-value.bottom-border::text")[5].get().strip().split(",")[1] 
            rom = response.css("tr.RowBG2 td.fasla.RowBG1.specs-value.bottom-border::text")[5].get().strip().split(",")[0]  
            os = response.css("td.fasla.RowBG1.specs-value.bottom-border::text").get().strip()
        
            yield{
                "Model name ": model_name,
                "Price ": price,
                "RAM ": ram,
                "ROM ": rom,
                "OS ": os
            }