class Column():
    
    def __init__(self, name, data_type, length=None, null=False, default=None, primary_key=False):
        self.name = name
        self.data_type = data_type
        self.length = length
        self.null = null
        self.default = default
        self.primary_key = primary_key
    
    ''' Getters and Setters '''
    
    # Name
    def get_name(self):
        return self.name
    
    def set_name(self, name):
        self.name = name
        
    # Data Type
    def get_data_type(self):
        return self.data_type
    
    def set_data_type(self, data_type):
        self.data_type = data_type
        
    # Length
    def get_length(self):
        return self.length
    
    def set_length(self, length):
        self.length = length
        
    # Null
    def get_null(self):
        return self.null
    
    def set_null(self, null):
        self.null = null
    
    # Default
    def get_default(self):
        return self.default
    
    def set_default(self, default):
        self.default = default
    
    # Primary Key
    def get_primary_key(self):
        return self.primary_key
    
    def set_primary_key(self, primary_key):
        self.primary_key = primary_key
        
    ''' Helper Methods '''
    
    def to_dict(self):
        column = {
            'name': self.name,
            'data_type': self.data_type,
            'length': self.length,
            'null': self.null,
            'default': self.default,
            'primary_key': self.primary
        }
        return column
    
    def length_string(self):
        if self.get_length() is not None:
            return "({length})".format(length=self.get_length())
        else:
            return ""
    
    def primary_key_string(self):
        if self.get_primary_key() is True:
            return " AUTO_INCREMENT PRIMARY KEY"
        else:
            return ""
    
    def null_string(self):
        if self.get_null() is True:
            return " NULL"
        elif self.get_null() is False:
            return " NOT NULL"
        else:
            return ""
        
    def default_string(self):
        if self.get_default() is not None:
            return " DEFAULT '{default}'".format(default=self.get_default())
        else:
            return ""
    
    def get_sql_string(self):
        query = "{name} {data_type}".format(name=self.get_name(), data_type=self.get_data_type())
        
        query += self.length_string()
        query += self.null_string()
        query += self.default_string()
        query += self.primary_key_string()
        
        return query
