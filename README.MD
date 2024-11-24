# RGB Pi Project

This is a simple Python script used to controle an RGB strip.
The hardware guide i used: Refer to "Resources used" section.

This script provides multiple modes and settings for those modes. The modes provide different colour patterns / transitions. I am still working on adding more.

Currently the whole script is being reworked to support multiple lights and different types. This will make the program need more configuration to get working but allows expandability.

## Currently whats complete is:
- Command System (Needs to be reworked).
- Settings (Needs to be reworked.).
- Controller (Getting reworked).
- Visualiser (Needs to be reworked no longer working.).
- Webpanel (Needs to be reworked no longer working.).

## TODO:
- Webpanel. Finish stylising.
- Add multi strip support. Control multiple type of LED Strips inderpendently.
- Add WS2812 support for addressible LEDS.
- Add These Modes: Sound React. Colour 1 2 Step.
- Add input support. GPIO Buttons, brightness sensors, Any form of input really. 
- Fix saving when setting change for main config. Keeps getting overwritten. Prolly thread related. Maybe use events or lock writting and reading when performing actions?
- Add savable mode configs / presets.

The Visualiser is intended to speed up the process of creating patterns and testing them. So you can visually see what would happen.

## Why?: 
I wanna learn how to create lights and lighting systems for Live events. I wanna create a custom light fixture from scratch and control it using DMX. Alongside this i wanna create a Laser system similar to Pangolin or Laser world laser systems.

Also improve my electronics and software understanding this is technically my second project that used software to control hardware. The last one i did was all the way back at school. lol.

I am planning to do an addressible LED strip next. I maybe intergrate the controller for that project into this one. However this is only able to control none addressible LED strips from my understanding.

## Resources used:
- [Hardware guide here.](https://dordnung.de/raspberrypi-ledstrip/) 
- [What i used as a template.](https://github.com/dordnung/raspberrypi-ledstrip/tree/master) 
- [Class loading system.](https://stackoverflow.com/questions/3178285/list-classes-in-directory-python)
- [TKinter used for test GUI.](https://realpython.com/python-gui-tkinter/) 
- [WebServer Source.](https://pythonbasics.org/webserver/)
- [Tempeture Monitor.](https://search.brave.com/search?q=get+raspberry+pi+temperature&spellcheck=0&source=alteredQuery&summary=1&conversation=a01dc941af2d7d224f0a2c&summary_og=471790e94269a57f25bf41)
- [Hardware guide here](https://dordnung.de/raspberrypi-ledstrip/) 
- [WS281x hardware guide here](https://dordnung.de/raspberrypi-ledstrip/ws2812) 
- [WS281x Library Python](https://github.com/rpi-ws281x/rpi-ws281x-python) 
- [WS281x Library](https://github.com/jgarff/rpi_ws281x) 