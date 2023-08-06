from mysql.connector import connect


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