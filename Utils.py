def clamp(value, minValue, maxValue):#TODO shorten this later with min and max.
    if value >= maxValue:
        return maxValue
    elif value <= minValue:
        return minValue
    else:
        return value
