from .column import Column


class VarcharColumn(Column):
    
    def __init__(self, name, length=100, null=False, default=None):
        self.name = name
        self.data_type = 'VARCHAR'
        self.length = length
        self.null = null
        self.default = default
        self.primary_key = False