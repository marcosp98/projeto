import psycopg2
import os
from scrapy.exceptions import DropItem

class PostgresPipeline:
    def open_spider(self, spider):
        # Carregar as variáveis de ambiente para evitar credenciais no código
        self.endpoint = os.getenv('PG_ENDPOINT', "projetointegradoriv.crm2omwsyzt8.us-east-1.rds.amazonaws.com")
        self.port = os.getenv('PG_PORT', 5432)
        self.user = os.getenv('PG_USER', "postgres")
        self.password = os.getenv('PG_PASSWORD', "projetointegrador")
        self.dbname = os.getenv('PG_DBNAME', "projetointegrador")

        try:
            # Conectar ao PostgreSQL
            self.conn = psycopg2.connect(
                host=self.endpoint,
                port=self.port,
                database=self.dbname,
                user=self.user,
                password=self.password
            )
            self.cursor = self.conn.cursor()

            # Criar tabela se não existir
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS produtos (
                    id SERIAL PRIMARY KEY,
                    titulo TEXT,
                    link TEXT,
                    preco TEXT,
                    img TEXT,
                    nota TEXT,
                    qtd_aval TEXT
                );
            ''')
            self.conn.commit()

        except Exception as e:
            spider.logger.error(f"Erro ao conectar ao banco de dados: {e}")
            self.cursor = None  # Evita erro futuro

    def close_spider(self, spider):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()

    def process_item(self, item, spider):
        if self.cursor is None:
            raise DropItem(f"Erro ao inserir no banco de dados: Conexão não estabelecida.")

        try:
            # Inserir item no banco de dados
            self.cursor.execute('''
                INSERT INTO produtos (titulo, link, preco, img, nota, qtd_aval)
                VALUES (%s, %s, %s, %s, %s, %s);
            ''', (item['titulo'], item['link'], item['preco'], item['img'], item['nota'], item['qtd_aval']))

            self.conn.commit()
            return item

        except Exception as e:
            spider.logger.error(f"Erro ao inserir no banco de dados: {e}")
            raise DropItem(f"Erro ao inserir no banco de dados: {e}")
