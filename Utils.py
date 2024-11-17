def clamp(value, minValue, maxValue):
    return max(minValue, min(value, maxValue))


def moveTowards(value, toValue, step):#TODO maybe create a better version of this.
    if value < toValue:
        if value+step >= toValue:
            return toValue
        else:
            return value + step
    else:
        if value-step <= toValue:
            return toValue
        else:
            return value - step

def rgbInvert(red, green, blue):
    return (255-red, 255-green, 255-blue)