"""
Module      main.py
Author      2023-01-10 Charles Geiser (https://www.dodeka.ch)

Purpose     Shows how to retrieve the time via WIFI from an NTP server pool
            and how to automatically set the time correction for time zone 
            and daylight saving time.

             
Board       ESP8266
Firmware    micropython from https://micropython.org

References  https://www.webexhibits.org/daylightsaving/i.html
"""

import time, network, ntptime
from binascii import hexlify
from machine import Pin

SSID = 'Dodeka2G4'
PSK  = '5408EnnetbadenHoehtalstrasse13'
MY_HOSTNAME = 'ESP8266_GSR'
NTP_POOL    = 'ch.pool.ntp.org'
OFFSET_MEZ  = const(1 * 60 * 60)
OFFSET_MESZ = const(2 * 60 * 60)

LEDBUILTIN = const(2)
led = Pin(LEDBUILTIN, Pin.OUT)

"""
Set local time with correction for timezone and daylight saving. 
It is assumed that the time change takes place on the last 
Sunday in March and in October
https://www.webexhibits.org/daylightsaving/i.html
Begin DST: Sunday March   (31 - (5*y//4 + 4) mod 7) at 1h U.T.
End   DST: Sunday October (31 - (5*y//4 + 1) mod 7) at 1h U.T.
"""
def setLocalTime(secondsOffsetNormalTime, secondsOffsetSavingTime):
    timeNotSet = True
    count = 0
    while timeNotSet:
        try:
            ntptime.settime()       # set internal clock to UTC
            y = time.localtime()[0] # get time and extract year
            dstStart = time.mktime((y,  3, 31 - (5 * y // 4 + 4) % 7, 1,0,0,0,0,0))
            dstEnd   = time.mktime((y, 10, 31 - (5 * y // 4 + 1) % 7, 1,0,0,0,0,0))
            now = time.time() # get timestamp
            offset = secondsOffsetSavingTime if now >= dstStart and now <= dstEnd else secondsOffsetNormalTime
            ntptime.NTP_DELTA -= offset # adjust NTP_DELTA
            ntptime.settime() # set the time according to the time zone and daylight saving time offsets
            timeNotSet = False
        except:
            count += 1
            print ('trying to set time %2d' % count)
            time.sleep_ms(1000)

""" 
    Returns true when the specified time has elapsed
    msCycle = [msPrevious, msCycle] is a globally defined list
    which holds the previous ticks_ms and the ms to wait
"""
def waitIsOver(msCycle):
    if (time.ticks_ms() - msCycle[0] >= msCycle[1]):
        msCycle[0] = time.ticks_ms()
        return True
    else:
        return False
"""
    Shows the WLANs visible in the vicinity as the tuple
    (ssid, bssid, channel, RSSI, security, hidden)
    security: 0 – open, 1 – WEP, 2 – WPA-PSK, 3 – WPA2-PSK, 4 – WPA/WPA2-PSK
    hidden: 0 or 1
"""
def showNearbyWlans(wlan):
    nearbyWlans = wlan.scan()
    for w in nearbyWlans:
        SSID, MAC, CHN, RSSI, SEC, HID = w
        MAC = hexlify(MAC, ':')
        ww = (SSID, MAC, CHN, RSSI, SEC, HID)
        print('SSID=%-32s, MAC=%s, CHN=%2d, RSSI=%d, SEC=%d, HID=%d' % ww)
    print()


wlan = network.WLAN(network.STA_IF)
wlan.config(dhcp_hostname = MY_HOSTNAME)
wlan.active(True)
if not wlan.isconnected():
    print('\n\nConnecting to WLAN ... ', end='')
    wlan.connect(SSID, PSK)
    while not wlan.isconnected():
        pass
print('connected as %s with IP %s\n' % (wlan.config('dhcp_hostname'), wlan.ifconfig()[0]))   

print('Nearby WLANs\n------------')
showNearbyWlans(wlan)

ntptime.host = NTP_POOL
setLocalTime(OFFSET_MEZ, OFFSET_MESZ)

msClockCycle = [0, 1000]

while True:
    if waitIsOver(msClockCycle):
        led.value(not led.value() )
        t = time.localtime() # (year, month, month-day, hour, min, second, weekday, year-day)
        print('%4d-%02d-%02d %02d:%02d:%02d\r' % t[0:6], end='') # display time on same line
    