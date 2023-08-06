from .column import Column


class IntColumn(Column):
    
    def __init__(self, name, length=11, null=False, default=None, primary_key=False):
        self.name = name
        self.data_type = 'INT'
        self.length = length
        self.null = null
        self.default = default
        self.primary_key= primary_key
