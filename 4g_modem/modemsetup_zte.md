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

## Also setup:

1. run `lsusb` to get ID

```
$ lsusb
Bus 001 Device 007: ID 19d2:1403 ZTE WCDMA Technologies MSM ZTE Technologies MSM
Bus 001 Device 003: ID 0424:ec00 Microchip Technology, Inc. (formerly SMSC) SMSC9512/9514 Fast Ethernet Adapter
Bus 001 Device 002: ID 0424:9514 Microchip Technology, Inc. (formerly SMSC) SMC9514 Hub
Bus 001 Device 001: ID 1d6b:0002 Linux Foundation 2.0 root hub
```

we take the `19d2` and `1403`.

2. Go to /lib/udev/rules.d/40-usb_modeswitch.rules and add the following entry:

```
# ZTE MF821 4G LTE
ATTRS{idVendor}=="19d2", ATTRS{idProduct}=="1403", RUN+="usb_modeswitch '%b/%k'"
```

3. Create file called: `19d2:1403` (`{idVendor}:{idProduct}`) in `/etc/usb_modeswitch.d/` and add the following inside that file:

```
# ZTE LTE 4g modem
#
DefaultVendor=  0x19d2
DefaultProduct= 0x1403

TargetVendor=  0x19d2
TargetProduct= 0x1403

MessageContent="55534243123456782400000080000685000000240000000000000000000000"

CheckSuccess=20
```

4. Make network manager recognize the device automatically. add this line to your `/etc/rc.local`

```
modprobe usbserial vendor=0x19d2 product=0x1403
```
