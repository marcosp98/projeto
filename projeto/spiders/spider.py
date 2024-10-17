import scrapy
from datetime import datetime


desejo = input("O que você deseja?")
data_pesquisa = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

class MLSpider(scrapy.Spider):
    name = 'mercadolivre'
    allowed_domains = ['mercadolivre.com.br'] #['kabum.com.br']
    start_urls = ['https://lista.mercadolivre.com.br/'+ desejo]#['https://www.kabum.com.br/hardware/memoria-ram']
    
    def parse(self, response):
        print("[ parse ]")
        produtos = response.css('li.ui-search-layout__item')
        
        for produto in produtos:
            titulo = produto.css('h2.poly-component__title a::text').get()
            link = produto.css('h2.poly-component__title a::attr(href)').get()
            reais = produto.css('.andes-money-amount__fraction::text').get()
            centavos = produto.css('.andes-money-amount__cents::text').get()
            preco = f"{reais},{centavos}" if centavos else f"{reais}"
            imagem_url = produto.css('img.poly-component__picture::attr(src)').get()
            nota_avaliacao = produto.css('span.poly-component__rating-number::text').get()
            quantidade_opinioes = produto.css('span.poly-component__reviews-amount::text').get()
            
            yield {
                'titulo': titulo,
                'link': link,
                'preco': preco,
                'img': imagem_url,
                'nota': nota_avaliacao,
                'data_pesquisa': data_pesquisa,
                'qtd_aval': quantidade_opinioes
            }
            
            
        next_page = response.css('li.andes-pagination__button--next a::attr(href)').get()

        if next_page:
            next_page_url = response.urljoin(next_page)  # Garante que a URL seja absoluta
            yield scrapy.Request(url=next_page_url, callback=self.parse, dont_filter=True)


