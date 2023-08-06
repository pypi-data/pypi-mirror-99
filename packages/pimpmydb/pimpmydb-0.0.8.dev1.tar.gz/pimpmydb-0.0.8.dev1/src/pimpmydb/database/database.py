from mysql.connector import connect
from ..tables import Table


class Database():
    
    def __init__(self):
        self.host = 'localhost'
        self.user = 'tester'
        self.password = 'PyTester123'
        self.database = 'pimpmydb_db'
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