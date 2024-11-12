from CommandBase import *

class ModeCommand(CommandBase):

    def __init__(self):
        super().__init__("Mode", "View and Change current RGB mode is running.")

    def execute(self, args, rgbController, cmdMan):
        if len(args) == 5:
            if args[1] in ["s", "setting"]:#Set or change the setting in the current mode.
                if args[2] in ["s", "set"]:
                    currentMode = rgbController.getCurrentMode()
                    if currentMode == None:
                        print("There is mode currently running on the controller.")
                        return

                    setting = currentMode.getSetting(args[3])
                    if setting == None:
                        print("Failed to find the setting... Check your spelling and check if this setting exists.")
                        return

                    if setting.getValueType() is int:
                        try:
                            intValue = int(args[4])
                            setting.setValue(floatValue)
                            print("Mode: {name} - {settingName} set to {newValue}".format(name = currentMode.getName(), settingName = setting.getName(), newValue = intValue))
                            rgbController.save()
                        except Exception as err:
                            print("Failed to cast the given value to a integer. With error message.\n\n{error}".format(error=err))

                    elif setting.getValueType() is float:
                        try:
                            floatValue = float(args[4])
                            setting.setValue(floatValue)
                            print("Mode: {name} - {settingName} set to {newValue}".format(name = currentMode.getName(), settingName = setting.getName(), newValue = floatValue))
                            rgbController.save()
                        except Exception as err:
                            print("Failed to cast the given value to a float. With error message.\n\n{error}".format(error=err))

                    elif setting.getValueType() is bool:
                        if args[4].lower() in ["1", "true"]:
                            setting.setValue(True)
                            print("Mode: {name} - {settingName} set to True".format(name = currentMode.getName(), settingName = setting.getName()))
                            rgbController.save()
                        elif args[4].lower() in ["0", "false"]:
                            setting.setValue(False)
                            print("Mode: {name} - {settingName} set to False".format(name = currentMode.getName(), settingName = setting.getName()))
                            rgbController.save()
                        else:
                            print("The given value of {valueArg} is invalid.".format(valueArg=args[4]))
                    else:
                        print("Unknown value type can change this value.")
                    return

        if len(args) == 3:
            if args[1] in ["c", "change", "s", "set"]:#Change or set the new mode.
                newMode = rgbController.getModes()[args[2].lower()]
                if newMode == None:
                    print("Given arguments failed to find a mode under the name of {name} nothing will be done.".format(name=args[2]))
                    return
                rgbController.setCurrentMode(newMode)
                print("Changed RGB Controller mode to {name}.".format(name=newMode.getName()))
                return

        if len(args) == 2:#Stop the current mode.
            if args[1] in ["s","stop"]:
                rgbController.setCurrentMode(None)
                return
            elif args[1] in ["l", "list"]:
                print("Listing all available modes...")
                for x in rgbController.getModes():
                    print("-{name}".format(name = x))
                return
            elif args[1] in ["set","settings"]:# View settings in the current mode.
                currentMode = rgbController.getCurrentMode()
                if currentMode == None:
                    print("There is no mode running on the RGB Controller currently.")
                    return
                
                settings = currentMode.getSettings()
                if len(settings) == 0:
                    print("The current mode has no settings.")
                    return 

                print("Displaying the current modes settings and values:\nName | Value")
                for x in settings:
                    print("-{name} > {value}".format(name=x.getName(), value=x.getValue()))
                return
        else:
            currentMode = rgbController.getCurrentMode()
            if currentMode == None:
                print("There is no mode running.")
            else:
                print("The RGB Controller is currently running: {name}".format(name=currentMode.getName()))


