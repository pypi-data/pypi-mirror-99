from ..fields import Field


class Form():
    
    def __init__(self, name, fields):
        self.name = name
        self.fields = fields
        
    def get_name(self):
        return self.name
    
    def set_name(self, name):
        self.name = name
        
    def get_fields(self):
        return self.fields
    
    def set_fields(self, fields):
        self.fields = fields
        
    ''' Helper Methods '''
    
    def to_dict(self):
        form = {
            'name': self.name,
            'fields': self.fields
        }
        return form
    
    ''' Form Processing Methods '''
    
    def get_field_values(self):
        values = []
        
        for field in self.fields:
            values.append(field.get_value())
        
        return values
    
    def validate(self):
        validation_results = []
        
        for field in self.fields:
            name = field.get_name()
            valid = field.validate()
            
            validation_result = {
                'name': name,
                'valid': valid
            }
            
            validation_results.append(validation_result)
            
        return validation_results