class StatementGenerator():
    
    def __init__(self, table_name):
        self.table_name = table_name
    
    def get_columns(self, data): # should be a dictionary
        columns = []
        
        for key in data:
            columns.append(key)
            
        return columns
    
    def get_values(self, data): # should be a dictionary
        values = []
        
        for key in data:
            values.append(data[key])
            
        return values
    
    def generate_insert_statement(self, data): # should be a dictionary
        statement_str = "INSERT INTO {table} (".format(table=self.table_name)
        
        columns = self.get_columns(data)
        for column in columns:
            column_str = "{column} {value}".format(column=column)
            
            if columns.index(column) == len(columns) - 1:
                column_str += ") VALUES ("
            else:
                column_str += ", "
            
            statement_str += column_str
            
        values = self.get_values(data)
        for value in values:
            value_str = "%s"
            
            if values.index(value) == len(values) - 1:
                value_str += ")"
            else:
                value_str += ", "
            
            statement_str += value_str
            
        return statement_str
    
    def generate_update_statement(self, data, record_id):
        statement_str = "UPDATE {table} SET ".format(table=self.table_name)
        
        columns = self.get_columns(data)
        for column in columns:
            column_str = "{column}=%s".format(column=column)
            
            if columns.index(column) == len(columns) - 1:
                column_str += " WHERE id={record_id}".format(record_id=record_id)
            else:
                column_str += ", "
            
            statement_str += column_str
        
        return statement_str
    
    def generate_delete_statement(self, record_id):
        statement_str = "DELETE FROM {table} WHERE id={record_id}".format(table=self.table_name, record_id=record_id)
        
        return statement_str