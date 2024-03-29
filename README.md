# Boge

Raspberry Pi Hardware project of Autumn 2023!

## Idea

- Be able to switch a 12V waterpump
- Read voltage of the 12V battery the pump + rpi is connected to
- Read if relay is on or not
- Read air humidity + temp
- Read soil moisture

Everything be remotly accessible 

## Docker

install docker:

https://docs.docker.com/engine/install/debian/

## Todo

Phase 1

- [X] Update backend to return all sensor values
- [X] Update HTML to pull backend for values every second
- [X] Move to docker container
- [X] Create docker-compose with backend + nginx with basic auth & ssl
- [X] Add some nice CSS

Phase 2

- [X] Start testing 4G modem

~~- Setup so RPi connects to dyndns service on boot~~

- Setup ssh tunnle on boot to sshserver

ssh-server:
- install:
    - nginx
    - certbot

- setup cert:
    
    `sudo certbot certonly --standalone -d example.com -d www.example.com`

    Stored here:
    - /etc/letsencrypt/live/<domain>/fullchain.pem
    - /etc/letsencrypt/live/<domain>/privkey.pem


## Wiring

Can be found [here](./wiring.md)

### How should things be connected at the place?

The white connector has four inputs:

```
[White] [Black] [Black] [White]
    1      2       3       4
```

1 = Incoming 12V via fuse
2 = Ground
3 = Ground
4 = Incoming 12V via fuse

12 Battery:
  - + goes to inline fuse -> 4
  - + goes to linline fuse -> 1
  - - goes to 3

Water pump:
  - Pin 87 on relay (the pin not shoed) is 12V+
  - Connect pump negative to ground


## Preview

![](./web.png)

![](./mobile.png)

## Connect ssh

1. ssh into bastion host on @sshserver.local

2. From that, ssh via tunnel on @localhost -p <port>

## Home assistant setup

configuration.yaml needs this:

```
http:
  use_x_forwarded_for: true
  trusted_proxies:
    - 127.0.0.1
    - ::1
```

## mqtt

Create password for user:

1. exec into mqtt container

2. run

    ```bash
    mosquitto_passwd -c /mosquitto/config/password.txt sensors
    ```

## Influx

- bucket needs to be named "Home Assistant"
- username and password is for connecting to UI
- Home assistnat should connect using token
- Token can be found in influxdb config file that is generated during boot

Config looks something like this:
```
[default]
  url = "http://localhost:8086"
  token = "<TOKEN>"
  org = "home_assistant"
  active = true
#
# [eu-central]
#   url = "https://eu-central-1-1.aws.cloud2.influxdata.com"
#   token = "XXX"
#   org = ""
#
# [us-central]
#   url = "https://us-central1-1.gcp.cloud2.influxdata.com"
#   token = "XXX"
#   org = ""
#
# [us-west]
#   url = "https://us-west-2-1.aws.cloud2.influxdata.com"
#   token = "XXX"
#   org = ""
```

# TODO:

- skriv upp hur saker ska kopplas in
- Mounta upp log-filerna från alla containerar så att de sparas på pien
