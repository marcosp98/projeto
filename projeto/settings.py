BOT_NAME = "projeto"

SPIDER_MODULES = ["projeto.spiders"]
NEWSPIDER_MODULE = "projeto.spiders"
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36'



ROBOTSTXT_OBEY = False

FEEDS = {
    'output/produtos.csv': {
        'format': 'csv',
        'encoding': 'utf8',
        'fields': ['id', 'titulo', 'link', 'preco', 'img', 'nota', 'qtd_aval', 'site'],
        'overwrite': False,  
    }
}

ITEM_PIPELINES = {
    'projeto.pipelines.CsvPipeline': 1,  
}

REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"

DOWNLOAD_DELAY = 2  # Atraso de 2 segundos entre cada request
