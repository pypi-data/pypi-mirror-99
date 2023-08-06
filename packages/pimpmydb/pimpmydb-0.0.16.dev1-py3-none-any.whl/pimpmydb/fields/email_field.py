from .field import Field


class EmailField(Field):
    
    def __init__(self, name, value):
        self.name = name
        self.data_type = 'email'
        self.value = value
        self.min_length = 3
        self.max_length = 255
