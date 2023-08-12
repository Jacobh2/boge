# Modem Setup

[taken from here](https://github.com/Ricram2/USBModem-LTE-3G-4G-Raspberry-Raspbian-/tree/master)

1. `sudo apt-get install usb-modeswitch usb-modeswitch-data modemmanager`

2. `sudo apt-get install wvdial minicom`

3. In `/etc/wvdial.conf` add

```
[Dialer Defaults]
Init1 = ATZ
Init2 = ATQ0 V1 E1 S0=0 &C1 &D2 +FCLASS=0

#Replace "internet.comcel.com.co" for APN 
Init3 = AT+CGDCONT=1,"IP","<APN FROM PROVIDER>"

#Replace for the ones specific to your carrier
Username = 
Password = 
Phone = *99#

Modem Type = Analog Modem
Stupid Mode = on
Baud = 9600
New PPPD = yes
Dial Command = ATDT

#Replace for wherever your USB STICK MODEM is mounted 
Modem = /dev/ttyUSB2
ISDN = 0
```

4. `sudo chmod +x usbconnect.sh`

5. `sudo ./usbconnect.sh`

6. `route add default dev ppp0`