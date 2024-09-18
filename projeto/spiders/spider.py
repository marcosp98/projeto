import scrapy

class KabumSpider(scrapy.Spider):
    name = 'kabum'
    allowed_domains = ['mercadolivre.com.br'] #['kabum.com.br']
    start_urls = ['https://lista.mercadolivre.com.br/memoria-ram#D[A:memoria%20ram]']#['https://www.kabum.com.br/hardware/memoria-ram']
    id_counter = 1

    def parse(self, response):
        print("[ parse ]")
        produtos = response.css('li.ui-search-layout__item')
        
        for produto in produtos:
            titulo = produto.css('h2.ui-search-item__title a::text').get()
            link = produto.css('a.ui-search-link::attr(href)').get()
            reais = produto.css('.andes-money-amount__fraction::text').get()
            centavos = produto.css('.andes-money-amount__cents::text').get()
            preco = f"{reais},{centavos}" if centavos else f"{reais}"
            imagem_url = produto.css('img.ui-search-result-image__element::attr(src)').get()

            yield {
                'id': self.id_counter,
                'titulo': titulo,
                'link': link,
                'preco': preco,
                'img': imagem_url
            }
            self.id_counter += 1
            
            # print(f"Título: {titulo}")
            # print(f"Link: {link}")
            # print(f"Preço: R$ {preco}")
            # print(f"Imagem URL: {imagem_url}")

        next_page = response.css('a.andes-pagination__link::attr(href)').get()
        if next_page:
            # Converte o link relativo para uma URL absoluta
                next_page_url = response.urljoin(next_page)
                yield response.follow(next_page_url, self.parse)