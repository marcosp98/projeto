import csv
import os

class CsvPipeline:
    def __init__(self):
        self.file_path = 'output/produtos.csv'
        
        # Verificar se o arquivo já existe e tem conteúdo
        if os.path.exists(self.file_path):
            with open(self.file_path, 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                rows = list(reader)
                # Continua a contagem de IDs a partir da última linha do CSV (se houver)
                if len(rows) > 1:
                    self.id_counter = len(rows)  # Inicia o ID a partir do último valor
                else:
                    self.id_counter = 1  # Começa do 1 se o CSV estava vazio
        else:
            self.id_counter = 1  # Começa do 1 se o CSV não existe
        
        # Abre o arquivo para adicionar novos dados
        self.file = open(self.file_path, 'a', newline='', encoding='utf-8')
        self.writer = csv.writer(self.file)

        # Se o arquivo estava vazio, escreve o cabeçalho
        if os.stat(self.file_path).st_size == 0:
            self.writer.writerow(['id', 'titulo', 'link', 'preco', 'img', 'nota', 'qtd_aval'])  # Cabeçalho

    def process_item(self, item, spider):
        # Atribuir o ID ao item e escrever no CSV
        item['id'] = self.id_counter
        item['site'] = spider.allowed_domains[0]  # Capturar o site (domínio) da spider
        self.writer.writerow([item['id'], item['titulo'], item['link'], item['preco'], item['img'], item['nota'], item['qtd_aval'], item['site']])
        self.id_counter += 1  # Incrementar o ID para o próximo item
        return item

    def close_spider(self, spider):
        self.file.close()
