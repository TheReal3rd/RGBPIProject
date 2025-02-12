from Visualiser.Components.ComponentBase import *

class DropDownComponent(ComponentBase):

    _dropDownValues = None
    _dropDownValueIndex = None

    _focus = False

    def __init__(self, name, position, size, valuesArr, valueIndex, includeNone=True):
        super().__init__(name, position, size)

        self._dropDownValues = valuesArr
        self._dropDownValueIndex = valueIndex
        self._focus = False

        if includeNone:
            if not "None" in valuesArr:
                valuesArr.append("None")
            if valueIndex == None or valueIndex == -1:
                self._dropDownValueIndex  = len(valuesArr) - 1




