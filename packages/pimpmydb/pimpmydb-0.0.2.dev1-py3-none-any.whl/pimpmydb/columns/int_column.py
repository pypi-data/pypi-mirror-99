from .column import Column


class IntColumn(Column):
    
    def __init__(self, name, length=11, null=False, default=None, primary_key=False):
        self.name = name
        self.data_type = 'INT'
        self.length = length
        self.null = null
        self.default = default
        self.primary_key= primary_key
        
    def get_sql_string(self):
        query = "{name} {data_type}".format(name=self.get_name(), data_type=self.get_data_type())
        
        query += self.length_string()
        query += self.null_string()
        query += self.default_string()
        query += self.primary_key_string()
        
        return query