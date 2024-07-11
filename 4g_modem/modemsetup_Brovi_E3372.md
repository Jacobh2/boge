1. run `lsusb` to get ID

```
~ $ lsusb
Bus 001 Device 008: ID 3566:2001 Mobile Mobile
Bus 001 Device 003: ID 0424:ec00 Microchip Technology, Inc. (formerly SMSC) SMSC9512/9514 Fast Ethernet Adapter
Bus 001 Device 002: ID 0424:9514 Microchip Technology, Inc. (formerly SMSC) SMC9514 Hub
Bus 001 Device 001: ID 1d6b:0002 Linux Foundation 2.0 root hub
```

we take the `3566` & `2001`.

2. Create file `/etc/udev/rules.d/40-huawei.rules` and add the following:

```
# This is part of USB_ModeSwitch version 1.x.x
#
ACTION!="add", GOTO="modeswitch_rules_end"
SUBSYSTEM!="usb", GOTO="modeswitch_rules_end"

# All known install partitions are on interface 0
ATTRS{bInterfaceNumber}!="00", GOTO="modeswitch_rules_end"

# only storage class devices are handled; negative
# filtering here would exclude some quirky devices
ATTRS{bDeviceClass}=="e0", GOTO="modeswitch_rules_begin"
ATTRS{bInterfaceClass}=="e0", GOTO="modeswitch_rules_begin"
GOTO="modeswitch_rules_end"

LABEL="modeswitch_rules_begin"
# Huawei E3372-325
ATTRS{idVendor}=="3566", ATTRS{idProduct}=="2001", RUN+="/sbin/usb_modeswitch -v 3566 -p 2001 -W -R -w 400"
ATTRS{idVendor}=="3566", ATTRS{idProduct}=="2001", RUN+="/sbin/usb_modeswitch -v 3566 -p 2001 -W -R"

LABEL="modeswitch_rules_end"
```

3. Create file called `3566:2001` (`{idVendor}:{idProduct}`) in `/etc/usb_modeswitch.d/` and add the following inside that file:

```
#Brovi E3372
TargetVendor=0x3566
TargetProductList="1506"
HuaweiNewMode=1
NoDriverLoading=1
```

3. Make network manager recognize the device automatically. add this line to your `/etc/rc.local`

```
modprobe usbserial vendor=0x3566 product=0x2001
```