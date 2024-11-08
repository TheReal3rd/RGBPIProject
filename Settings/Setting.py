

class Setting():
    _name = None 
    _value = None
    _valueType = None
    _description = None

    def __init__(self, name, description, value, valueType):
        self._name = name
        self._description = description
        self._value = value
        self._valueType = valueType

    #Getters
    def getName(self):
        return self._name

    def getDescription(self):
        return self._description

    def getValue(self):
        return self._value

    def getValueType(self):
        return self._valueType

    #Setters

    def setValue(self, newValue):
        self._value = newValue

    #Data

    def save(self):
        pass

    def load(self):
        pass
    
