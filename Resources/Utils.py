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

def fetchDeviceTemps():# This is intended to run on Pi so i only gonna write this for the Pi.
    import platform
    if "Raspbian" in platform.version():
        import subprocess
        temp = subprocess.check_output(["vcgencmd", "measure_temp"])
        return temp.decode().strip().split("=")[1]
    else:
        return "-1"

def keysWithinDictCheck(keysArr, dict):
    for key in keysArr:
        if not key in dict.keys():
            return False
    return True

class msDelay():
    startMs = 0

    def __init__(self):
        import time
        self.startMs = int(round(time.time() * 1000))

    def reset(self):
        self.startMs = int(round(time.time() * 1000))

    def passedMS(self, amount):
        if(self.startMs >= amount):
            return True
        return False

    def passedMSReset(self, amount):
        if self.passedMS(amount):
            self.reset()
            return True
        return False
            
