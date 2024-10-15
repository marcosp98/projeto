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
# import pyodbc
# from scrapy.exceptions import DropItem

# class SQLServerPipeline:

#     def open_spider(self, spider):
#         # Configura a conexão com o banco de dados SQL Server
#         self.conn = pyodbc.connect(
#             'DRIVER={ODBC Driver 17 for SQL Server};'
#             'SERVER=192.168.0.100,1433;'
#             'DATABASE=ProjetoSCLPM;'
#             'UID=admin;'
#             'PWD=projetof@tec2024'
#         )
#         self.cursor = self.conn.cursor()
        
#         # Crie a tabela se ela não existir
#         self.cursor.execute('''
#             IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='produtos' AND xtype='U')
#             CREATE TABLE produtos (
#                 id INT IDENTITY(1,1) PRIMARY KEY,
#                 titulo NVARCHAR(255),
#                 link NVARCHAR(MAX),
#                 preco NVARCHAR(50),
#                 img NVARCHAR(MAX),
#                 nota NVARCHAR(10),
#                 qtd_aval NVARCHAR(10)
#             )
#         ''')
#         self.conn.commit()

#     def close_spider(self, spider):
#         self.conn.close()

#     def process_item(self, item, spider):
#         # Inserir os dados no banco de dados
#         self.cursor.execute('''
#             INSERT INTO produtos (titulo, link, preco, img, nota, qtd_aval)
#             VALUES (?, ?, ?, ?, ?, ?)
#         ''', 
#         (item['titulo'], item['link'], item['preco'], item['img'], item['nota'], item['qtd_aval']))
        
#         self.conn.commit()
#         return item
