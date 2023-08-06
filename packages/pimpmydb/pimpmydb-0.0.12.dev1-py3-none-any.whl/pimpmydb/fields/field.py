class Field():
    
    def __init__(self, name, value):
        self.name = name
        self.value = value
        
    ''' Getters and Setters '''
    
    def get_name(self):
        return self.name
    
    def set_name(self, name):
        self.name = name
        
    def get_value(self):
        return self.value
    
    def set_value(self, value):
        self.value = value
        
    ''' Helper Methods '''
    
    def to_dict(self):
        field = {
            'name': self.name,
            'value': self.value
        }
        return field
