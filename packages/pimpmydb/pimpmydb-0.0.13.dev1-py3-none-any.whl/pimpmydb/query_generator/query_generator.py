from ..tables import Table


class QueryGenerator():
    
    def __init__(self, table_name):
        self.table_name = table_name
        
    def generate_select_all_query(self):
        ''' Generates an SQL query that selects all records in a table '''
        
        return "SELECT * FROM {table}".format(table=self.table_name)
    
    def generate_select_by_id_query(self, record_id):
        ''' Generates an SQL query that selects a single record by its id '''
        
        return "SELECT * FROM {table} WHERE id={record_id} LIMIT 1".format(table=self.table_name, record_id=record_id)
    
    def generate_select_by_column(self, column, value):
        ''' Generates an SQL query that selects all records whose specified column matches the search value '''
        
        return "SELECT * FROM {table} WHERE {column}='{value}'".format(table=self.table_name, column=column, value=value)