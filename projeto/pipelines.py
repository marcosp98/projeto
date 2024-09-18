# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import sqlite3
from scrapy.exceptions import DropItem

class DatabasePipeline:

    def open_spider(self, spider):
            self.conn = sqlite3.connect('produtos.db')
            self.cursor = self.conn.cursor()
            # Crie a tabela se não existir
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS produtos (
                    id TEXT PRIMARY KEY,
                    titulo TEXT,
                    link TEXT,
                    preco REAL,  # Mude o tipo para REAL
                    imagem_url TEXT
                )
            ''')
            self.conn.commit()

    def close_spider(self, spider):
        self.conn.close()

    def process_item(self, item, spider):
        # Verifique se o ID já existe
        self.cursor.execute('SELECT id FROM produtos WHERE id = ?', (item['ID'],))
        result = self.cursor.fetchone()

        if result:
                # Se o ID já existir, não faça nada
            raise DropItem(f"Produto com ID {item['ID']} já existe")

            # Converta o preço para um valor numérico (float)
        preco = item['Preço'].replace(',', '.')  # Substitua ',' por '.'
        try:
            preco_valor = float(preco)
        except ValueError:
            raise DropItem(f"Preço inválido: {item['Preço']}")
            
            # Insira o novo produto
        self.cursor.execute('''
            INSERT INTO produtos (id, titulo, link, preco, imagem_url)
            VALUES (?, ?, ?, ?, ?)
        ''', (item['id'], item['titulo'], item['link'], preco_valor, item['img']))
        self.conn.commit()
        return item
        
ITEM_PIPELINES = {
    'your_project_name.pipelines.DatabasePipeline': 1,
}
