# NtpTime

The example program shows how to retrieve the time via WIFI from an NTP server pool 
and how to automatically set the time correction for time zone 
and daylight saving time when the corresponding time offsets are known.
The date of transition from standard time to daylight saving time is calculated 
using the formulas as explained [here](https://www.webexhibits.org/daylightsaving/i.html).

As a little extra the own hostname is set and the IP address is 
queried and also the active WLANs in the vicinity are listed.

Subsequently, the time is displayed every second, not on a new 
line each time, but always in the same place on the screen.

The output generated by the program is shown below. After the connection 
is established, the hostname and IP of the ESP8266 and the list of nearby 
WLANs are displayed. Then several attempts are made to retrieve the time 
from the NTP pool until this succeeds and the time is displayed continuously.
```
Connecting to WLAN ... connected as ESP8266_GSR with IP 192.168.9.44

Nearby WLANs
------------
SSID=b'UPC7465798'                   , MAC=b'34:2c:c4:12:08:27', CHN= 1, RSSI=-93, SEC=4, HID=0
SSID=b'Dodeka2G4'                    , MAC=b'34:31:c4:8b:ae:ec', CHN= 1, RSSI=-39, SEC=4, HID=0
SSID=b'UPC Wi-Free'                  , MAC=b'36:2c:94:12:08:27', CHN= 1, RSSI=-92, SEC=5, HID=0
SSID=b'bfi-45161'                    , MAC=b'dc:0b:1a:a8:e6:99', CHN= 6, RSSI=-87, SEC=2, HID=0
SSID=b'UPC Wi-Free'                  , MAC=b'de:53:1c:99:ee:e8', CHN= 6, RSSI=-93, SEC=5, HID=0
SSID=b'nadnet'                       , MAC=b'74:42:7f:21:3a:d5', CHN= 7, RSSI=-90, SEC=3, HID=0
SSID=b'Fido-I'                       , MAC=b'bc:cf:4f:fe:f6:b7', CHN=13, RSSI=-89, SEC=3, HID=0

trying to set time  1
trying to set time  2
trying to set time  3
2023-01-11 18:26:25
```

