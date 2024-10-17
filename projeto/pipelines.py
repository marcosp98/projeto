import psycopg2
import os
from scrapy.exceptions import DropItem

class PostgresPipeline:
    def open_spider(self, spider):
        self.endpoint = os.getenv('PG_ENDPOINT', "projetointegradoriv.crm2omwsyzt8.us-east-1.rds.amazonaws.com")
        self.port = os.getenv('PG_PORT', 5432)
        self.user = os.getenv('PG_USER', "postgres")
        self.password = os.getenv('PG_PASSWORD', "projetointegrador")
        self.dbname = os.getenv('PG_DBNAME', "projetointegrador")

        try:
            self.conn = psycopg2.connect(
                host=self.endpoint,
                port=self.port,
                database=self.dbname,
                user=self.user,
                password=self.password
            )
            self.cursor = self.conn.cursor()

            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS produtos(
                    id SERIAL PRIMARY KEY,
                    titulo TEXT,
                    link TEXT,
                    preco TEXT,
                    img TEXT,
                    nota TEXT,
                    qtd_aval TEXT,
                    data_pesquisa TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            ''')
            self.conn.commit()

        except Exception as e:
            spider.logger.error(f"Erro ao conectar ao banco de dados: {e}")
            self.cursor = None

    def close_spider(self, spider):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()

    def process_item(self, item, spider):
        if self.cursor is None:
            raise DropItem(f"Erro ao inserir no banco de dados: Conexão não estabelecida.")

        try:
            # Use item['field_name'] to access the data
            self.cursor.execute('''
                INSERT INTO produtos (titulo, link, preco, img, nota, qtd_aval, data_pesquisa)
                VALUES (%s, %s, %s, %s, %s, %s, %s);
            ''', (item.get('titulo'), item.get('link'), item.get('preco'), 
                  item.get('img'), item.get('nota'), item.get('qtd_aval'), 
                  item.get('data_pesquisa', None)))  # data_pesquisa pode ser opcional
            self.conn.commit()
            return item

        except Exception as e:
            spider.logger.error(f"Erro ao inserir no banco de dados: {e}")
            raise DropItem(f"Erro ao inserir no banco de dados: {e}")
