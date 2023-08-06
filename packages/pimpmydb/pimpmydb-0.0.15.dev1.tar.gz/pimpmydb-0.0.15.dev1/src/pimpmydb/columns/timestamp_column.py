from .column import Column


class TimestampColumn(Column):
    
    def __init__(self, name, null=True, default=None):
        self.name = name
        self.data_type = 'TIMESTAMP'
        self.length = None
        self.null = null
        self.default = default
        self.primary_key = False