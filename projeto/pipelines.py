import csv
import os

class CsvPipeline:
    def __init__(self):
        self.file_path = 'output/produtos.csv'
        
        # Verificar se o arquivo existe e tem conteúdo
        if os.path.exists(self.file_path):
            with open(self.file_path, 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                # Conta o número de linhas no CSV, ignorando o cabeçalho
                rows = list(reader)
                if len(rows) > 1:  # Se tiver produtos no CSV
                    self.id_counter = len(rows)  # Continua a contagem
                else:
                    self.id_counter = 1  # Reinicia do 1
        else:
            self.id_counter = 1  # Reinicia do 1 se não houver arquivo

        # Abrir o arquivo para adicionar novos dados
        self.file = open(self.file_path, 'a', newline='', encoding='utf-8')
        self.writer = csv.writer(self.file)

        # Se o arquivo foi apagado, escrever o cabeçalho novamente
        if os.stat(self.file_path).st_size == 0:
            self.writer.writerow(['id', 'titulo', 'link', 'preco', 'img'])  # Cabeçalho

    def process_item(self, item, spider):
        item['id'] = self.id_counter  # Atribuir ID único
        self.writer.writerow([item['id'], item['titulo'], item['link'], item['preco'], item['img']])
        self.id_counter += 1
        return item

    def close_spider(self, spider):
        self.file.close()
