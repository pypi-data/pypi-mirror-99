from ..columns import *


class Table():
    
    def __init__(self, name, columns):
        self.name = name
        self.columns = columns
        
    def get_create_sql(self):
        sql_str = "CREATE TABLE {table} (".format(table=self.name)
        
        for column in self.columns:
            sql_str += column.get_sql_string()
            if self.columns.index(column) == len(self.columns) - 1:
                sql_str += ");"
            else:
                sql_str += ", "
        
        return sql_str
    
    def get_drop_table_sql(self):
        return "DROP TABLE {table}".format(table=self.name)
    
    def get_add_column_sql(self, column):
        return "ALTER TABLE ADD {column}".format(column=column.get_sql_string())
    
    def get_drop_column_sql(self, column):
        return "ALTER TABLE DROP COLUMN {column}".format(column=column.get_name())
    
    def get_modify_column_sql(self, column):
        return "ALTER TABLE MODIFY COLUMN {column}".format(column=column.get_sql_string())
