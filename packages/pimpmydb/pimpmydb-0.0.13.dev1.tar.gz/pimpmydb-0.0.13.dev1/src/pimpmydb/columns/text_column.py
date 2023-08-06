from .column import Column


class TextColumn(Column):
    
    def __init__(self, name, length=None, null=False, default=None):
        self.name = name
        self.data_type = 'TEXT'
        self.length = length
        self.null = null
        self.default = default
        self.primary_key = False