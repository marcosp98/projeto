# import scrapy

# desejo = input("O que você deseja?")

# class MLSpider(scrapy.Spider):
#     name = 'mercadolivre'
#     allowed_domains = ['mercadolivre.com.br'] #['kabum.com.br']
#     start_urls = ['https://lista.mercadolivre.com.br/'+ desejo]#['https://www.kabum.com.br/hardware/memoria-ram']
    
#     def parse(self, response):
#         print("[ parse ]")
#         produtos = response.css('li.ui-search-layout__item')
        
#         for produto in produtos:
#             titulo = produto.css('h2.ui-search-item__title a::text').get()
#             link = produto.css('a.ui-search-link::attr(href)').get()
#             reais = produto.css('.andes-money-amount__fraction::text').get()
#             centavos = produto.css('.andes-money-amount__cents::text').get()
#             preco = f"{reais},{centavos}" if centavos else f"{reais}"
#             imagem_url = produto.css('img.ui-search-result-image__element::attr(src)').get()
#             nota_avaliacao = produto.css('span.ui-search-reviews__rating-number::text').get()
#             quantidade_opinioes = produto.css('span.ui-search-reviews__amount::text').get()
            
#             yield {
#                 'titulo': titulo,
#                 'link': link,
#                 'preco': preco,
#                 'img': imagem_url,
#                 'nota': nota_avaliacao,
#                 'qtd_aval': quantidade_opinioes
#             }
            
            
#         next_page = response.css('li.andes-pagination__button--next a::attr(href)').get()

#         if next_page:
#             next_page_url = response.urljoin(next_page)  # Garante que a URL seja absoluta
#             yield scrapy.Request(url=next_page_url, callback=self.parse, dont_filter=True)
#             # print(f"Link: {link}")
#             # print(f"Preço: R$ {preco}")
#             # print(f"Imagem URL: {imagem_url}")

import scrapy


class VerificaRestricoesSpider(scrapy.Spider):
    name = "test"
    allowed_domains = [
        "amazon.com.br",
        "kabum.com.br",
        "pichau.com.br",
        "magazineluiza.com.br",
        "terabyte.com.br"
    ]
    start_urls = [
        "https://www.amazon.com.br/robots.txt",
        "https://www.kabum.com.br/robots.txt",
        "https://www.pichau.com.br/robots.txt",
        "https://www.magazineluiza.com.br/robots.txt",
        "https://terabyte.com.br/robots.txt"
    ]

    def parse(self, response):
        site = response.url
        self.logger.info(f"Verificando {site}")
        
        # Extrai o conteúdo do robots.txt
        conteudo = response.text.strip().splitlines()
        
        # Inicializa as listas de restrições
        allow = []
        disallow = []

        # Processa as linhas do robots.txt
        for linha in conteudo:
            linha = linha.strip()
            if linha.startswith("Allow:"):
                allow.append(linha[6:].strip())
            elif linha.startswith("Disallow:"):
                disallow.append(linha[9:].strip())

        # Exibe as restrições
        self.logger.info(f"Permissões em {site}: {allow}")
        self.logger.info(f"Restrições em {site}: {disallow}")

