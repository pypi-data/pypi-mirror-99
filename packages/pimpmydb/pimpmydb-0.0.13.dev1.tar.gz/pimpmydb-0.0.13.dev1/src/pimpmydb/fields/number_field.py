from .field import Field


class NumberField(Field):
    
    def __init__(self, name, value, min_number=None, max_number=None):
        self.name = name
        self.data_type = 'number'
        self.value = value
        self.min_number = min_number
        self.max_number = max_number
        
    def validate(self):
        return self.value_is_number()
        
    def value_is_number(self):
        if isinstance(self.value, int) or isinstance(self.value, float):
            return True
        else:
            return False