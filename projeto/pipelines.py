import os
import csv

class CsvPipeline:
    def __init__(self):
        self.file_path = 'output/produtos.csv'
        self.id_counter = 1

        # Verifica se o diretório output existe, se não, cria
        if not os.path.exists('output'):
            os.makedirs('output')

        # Abre o arquivo em modo append
        self.file = open(self.file_path, 'a', newline='', encoding='utf-8')
        self.writer = csv.writer(self.file)

        # Verifica se o arquivo já existe e não está vazio
        if os.path.getsize(self.file_path) == 0:  # Verifica se o arquivo está vazio
            self.writer.writerow(['id', 'titulo', 'link', 'preco', 'img'])  # Escreve o cabeçalho
        else:
            # Lê o último ID do arquivo para continuar a contagem
            self.id_counter = self.get_last_id()

    def get_last_id(self):
        with open(self.file_path, 'r', newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            last_row = list(reader)[-1]  # Lê a última linha do arquivo
            return int(last_row[0]) + 1  # Retorna o próximo ID

    def process_item(self, item, spider):
        item['id'] = self.id_counter  # Atribui o ID ao item
        self.writer.writerow([item['id'], item['titulo'], item['link'], item['preco'], item['img']])
        self.id_counter += 1  # Incrementa o contador do ID
        return item

    def close_spider(self, spider):
        # Fecha o arquivo quando o spider é fechado
        self.file.close()
