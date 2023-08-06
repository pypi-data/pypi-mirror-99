import os
from mysql.connector import connect
from dotenv import load_dotenv
from ..tables import Table

load_dotenv()


class Database():
    
    def __init__(self):
        self.host = os.getenv('DB_HOST')
        self.user = os.getenv('DB_USER')
        self.password = os.getenv('DB_PASSWORD')
        self.database = os.getenv('DB_NAME')
        self.connection = connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )
        
    def cursor(self):
        return self.connection.cursor()
    
    def create_table(self, table):
        sql_str = table.get_sql_string()
        
        cursor = self.connection.cursor()
        cursor.execute(sql_str)
        
        conn = self.connection
        conn.commit()