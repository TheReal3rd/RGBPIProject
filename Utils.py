def clamp(value, minValue, maxValue):
    return max(minValue, min(value, maxValue))


def moveTowards(value, toValue, step):
    if value+step > toValue:
        return toValue
    else:
        return value + step