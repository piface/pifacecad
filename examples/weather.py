#!/usr/bin/env python3
"""
Get your weather from a weather station just blocks from your home.
Go to http://www.wunderground.com/wundermap/ and find a weather station near
you. Click on a temperature bubble for that area. When the window pops up,
click on hypertext link with the station ID, then on the bottom right of the
page, click on the Current Conditions XML. Thats your link! Good luck!
"""

import sys
PY3 = sys.version_info[0] >= 3
if not PY3:
    print("Weather only works with `python3`.")
    sys.exit(1)

import urllib.request
import xml.etree.ElementTree
from time import sleep
from threading import Barrier
import pifacecommon
import pifacecad


UPDATE_INTERVAL = 60  # seconds

WEATHER_STATIONS = [
    {"location": "Oldham", "id": "IGREATER54"},
    {"location": "London", "id": "IGREATER13"},
    {"location": "Paris", "id": "IILEDEFR15"},
    {"location": "New York", "id": "KNYNEWYO62"},
]
URL_PREFIX = \
    "http://api.wunderground.com/weatherstation/WXCurrentObXML.asp?ID="

TEMP_SYMBOL = pifacecad.LCDBitmap([0x4, 0x4, 0x4, 0x4, 0xe, 0xe, 0xe, 0x0])
WIND_SYMBOL = pifacecad.LCDBitmap([0x0, 0xf, 0x3, 0x5, 0x9, 0x10, 0x0])
TEMP_SYMBOL_INDEX, WIND_SYMBOL_INDEX = 0, 1


class WeatherStation(object):
    def __init__(self, location, weather_id):
        self.location = location
        self.weather_id = weather_id
        self._xmltree = None

    def generate_xmltree(self):
        url = get_current_condition_url(self.weather_id)
        data = urllib.request.urlopen(url)
        self._xmltree = xml.etree.ElementTree.XML(data.read())

    @property
    def xmltree(self):
        """Only get xml info the first time we need it (WARNING: gets stale).
        """
        if self._xmltree is None:
            self.generate_xmltree()
        return self._xmltree

    @property
    def temperature(self):
        return self.xmltree.findall("temp_c")[0].text

    @property
    def wind_mph(self):
        return self.xmltree.findall("wind_mph")[0].text


class WeatherDisplay(object):
    def __init__(self, cad, stations, station_index=0):
        self.stations = stations
        self.station_index = station_index
        self.cad = cad
        self.cad.lcd.store_custom_bitmap(TEMP_SYMBOL_INDEX, TEMP_SYMBOL)
        self.cad.lcd.store_custom_bitmap(WIND_SYMBOL_INDEX, WIND_SYMBOL)
        self.cad.lcd.backlight_on()
        self.cad.lcd.blink_off()
        self.cad.lcd.cursor_off()

    @property
    def current_station(self):
        """Returns the current station dict."""
        return self.stations[self.station_index]

    def next_station(self, event=None):
        self.station_index = (self.station_index + 1) % len(self.stations)
        self.update()

    def previous_station(self, event=None):
        self.station_index = (self.station_index - 1) % len(self.stations)
        self.update()

    def update(self, event=None):
        self.current_station.generate_xmltree()  # before we print anything
        self.cad.lcd.clear()
        self.cad.lcd.write("{place}\n".format(
            place=self.stations[self.station_index].location))
        # temperature
        self.cad.lcd.write_custom_bitmap(TEMP_SYMBOL_INDEX)
        self.cad.lcd.write(":")
        self.cad.lcd.write("{temp}C ".format(
            temp=self.current_station.temperature))
        # wind
        self.cad.lcd.write_custom_bitmap(WIND_SYMBOL_INDEX)
        self.cad.lcd.write(":")
        self.cad.lcd.write("{wind}mph".format(
            wind=self.current_station.wind_mph))

    def close(self):
        self.cad.lcd.clear()
        self.cad.lcd.backlight_off()


def get_current_condition_url(weather_station_id):
    return "{prefix}{id}".format(prefix=URL_PREFIX, id=weather_station_id)


if __name__ == "__main__":
    stations = \
        [WeatherStation(s['location'], s['id']) for s in WEATHER_STATIONS]

    cad = pifacecad.PiFaceCAD()
    global weatherdisplay
    weatherdisplay = WeatherDisplay(cad, stations)
    weatherdisplay.update()

    # listener cannot deactivate itself so we have to wait until it has
    # finished using a barrier.
    global end_barrier
    end_barrier = Barrier(2)

    # wait for button presses
    switchlistener = pifacecad.SwitchEventListener(chip=cad)
    switchlistener.register(4, pifacecad.IODIR_ON, end_barrier.wait)
    switchlistener.register(5, pifacecad.IODIR_ON, weatherdisplay.update)
    switchlistener.register(
        6, pifacecad.IODIR_ON, weatherdisplay.previous_station)
    switchlistener.register(
        7, pifacecad.IODIR_ON, weatherdisplay.next_station)

    switchlistener.activate()
    end_barrier.wait()  # wait unitl exit

    # exit
    weatherdisplay.close()
    switchlistener.deactivate()
