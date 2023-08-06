from ..columns import *


class Table():
    
    def __init__(self, name, columns):
        self.name = name
        self.columns = columns
        
    def get_sql_string(self):
        sql_str = "CREATE TABLE {table} (".format(table=self.name)
        
        for column in self.columns:
            sql_str += column.get_sql_string()
            if self.columns.index(column) == len(self.columns) - 1:
                sql_str += ");"
            else:
                sql_str += ", "
        
        return sql_str