# coding: utf-8

# Python API for The Fucking Weather, version 1.0
# Copyright (C) 2009  Ian Weller <ian@ianweller.org>
# http://ianweller.org/thefuckingweather
#
# This program is free software. It comes without any warranty, to
# the extent permitted by applicable law. You can redistribute it
# and/or modify it under the terms of the Do What The Fuck You Want
# To Public License, Version 2, as published by Sam Hocevar. See
# http://sam.zoy.org/wtfpl/COPYING for more details.

"""Scrapes data from www.thefuckingweather.com for a given location."""

from optparse import OptionParser
import re
import urllib
import urllib2

RE_WEATHER = """<div><span class="small">(.*)</span></div>
<div id="content"><div class="large" >(\d*)&deg;\?!<br />
<br />(.*)</div><div  id="remark"><br />
<span>(.*)</span></div>"""

RE_FORECAST = """<div class="boxhead">
<h2>THE FUCKING FORECAST</h2>
</div>
<div class="boxbody">
<table><tr>
<td>DAY:</td>
<td class="center"><strong>(.{3})</strong></td>
<td class="center"><strong>(.{3})</strong></td>
</tr>
<tr>
<td>HIGH:</td><td class="center hot">(\d*)</td>\
<td class="center hot">(\d*)</td>
</tr>
<tr>
<td>LOW:</td><td class="center cold">(\d*)</td>\
<td class="center cold">(\d*)</td>
</tr>
<tr>
<td>FORECAST:</td><td class="center">(.*)</td><td class="center">(.*)</td></tr>
</table>
</div>"""

DEGREE_SYMBOL = "°"


class LocationError(StandardError):
    """
    The website reported a "WRONG FUCKING ZIP" error, which could mean either
    the server has no clue what to do with your location or that it messed up.
    """

    def __init__(self):
        StandardError.__init__(self, "WRONG FUCKING ZIP returned from website")


class ParseError(StandardError):
    """
    Something is wrong with the regexps or the site owner updated his template.
    """

    def __init__(self):
        StandardError.__init__(
            self, """Couldn't parse the website.
RE: %s

Please report what you did to get this error and this full Python traceback
to ian@ianweller.org. Thanks!""" % RE_WEATHER)


def get_weather(location, celsius=False):
    """
    Retrieves weather and forecast data for a given location.

    Data is presented in a dict with three main elements: "location" (the
    location presented by TFW), "current" (current weather data) and "forecast"
    (a forecast of the next two days, with highs, lows, and what the weather
    will be like).

    "current" is a dictionary with three elements: "temperature" (an integer),
    "weather" (a list of descriptive elements about the weather, e.g., "ITS
    FUCKING HOT", which may be coupled with something such as "AND THUNDERING";
    this element is named as such because it always begins with "ITS FUCKING")
    and "remark" (a string printed by the server which is meant to be witty but
    is often not. each to their own, I guess).

    "forecast" is a dictionary with two elements, 0 and 1 (both integers). Each
    of these is a dictionary which contains the keys "day" (a three-letter
    string consisting of the day of week), "high" and "low" (integers
    representing the relative extreme temperature of the day) and "weather" (a
    basic description of the weather, such as "Scattered Thunderstorms").

    The default is for temperatures to be in Fahrenheit. If you're so inclined,
    you can pass True as a second variable and get temperatures in Celsius.

    If you need a degree symbol, you can use thefuckingweather.DEGREE_SYMBOL,
    for your convenience.
    """
    # Retrieve yummy HTML
    query = {"zipcode": location}
    if celsius:
        query["CELSIUS"] = "yes"
    query_string = urllib.urlencode(query)
    url = "http://www.thefuckingweather.com/?" + query_string
    data = urllib2.urlopen(url).read()
    # Check for an error report
    if re.search("WRONG FUCKING ZIP", data):
        raise LocationError()
    # No error, so parse current weather data
    return_val = {"current": {}, "forecast": {0: {}, 1: {}}}
    weather_search = re.search(RE_WEATHER, data)
    if not weather_search:
        raise ParseError()
    return_val["location"] = weather_search.group(1)
    return_val["current"]["temperature"] = int(weather_search.group(2))
    return_val["current"]["weather"] = weather_search.group(3).split(
        "<br />")
    return_val["current"]["remark"] = weather_search.group(4)
    # Now parse the forecast data
    forecast_search = re.search(RE_FORECAST, data)
    if not forecast_search:
        raise ParseError()
    return_val["forecast"][0]["day"] = forecast_search.group(1)
    return_val["forecast"][0]["high"] = int(forecast_search.group(3))
    return_val["forecast"][0]["low"] = int(forecast_search.group(5))
    return_val["forecast"][0]["weather"] = forecast_search.group(7)
    return_val["forecast"][1]["day"] = forecast_search.group(2)
    return_val["forecast"][1]["high"] = int(forecast_search.group(4))
    return_val["forecast"][1]["low"] = int(forecast_search.group(6))
    return_val["forecast"][1]["weather"] = forecast_search.group(8)
    # I'm gonna have to jump!
    return return_val


def main():
    """
    This function is run when the python file is run from the command line. It
    prints content formatted somewhat like www.thefuckingweather.com. You can
    use the -c (--celsius) switch to return temperatures in Celsius.
    """
    usage = "usage: %prog [-c] location"
    parser = OptionParser(usage=usage)
    parser.add_option("-c", "--celsius", dest="celsius", help="return temp"+\
                      "eratures in Celsius (Fahrenheit without this switch",
                      action="store_true", default=False)
    (options, args) = parser.parse_args()
    if len(args) == 1:
        weather = get_weather(args[0], options.celsius)
        weather_tuple = (weather["location"],
                         weather["current"]["temperature"],
                         DEGREE_SYMBOL,
                         "\n".join(weather["current"]["weather"]),
                         weather["current"]["remark"],
                         weather["forecast"][0]["day"],
                         weather["forecast"][0]["high"],
                         weather["forecast"][0]["low"],
                         weather["forecast"][0]["weather"],
                         weather["forecast"][1]["day"],
                         weather["forecast"][1]["high"],
                         weather["forecast"][1]["low"],
                         weather["forecast"][1]["weather"])
        print """\
(%s)
%d%s?! %s
%s

Forecast
  Today (%s)
    High: %d
    Low: %d
    Weather: %s
  Tomorrow (%s)
    High: %d
    Low: %d
    Weather: %s""" % weather_tuple
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
