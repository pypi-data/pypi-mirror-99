from .field import Field


class TextField(Field):
    
    def __init__(self, name, value, min_length=None, max_length=None):
        self.name = name
        self.data_type = 'text'
        self.value = value
        self.min_length = min_length
        self.max_length = max_length