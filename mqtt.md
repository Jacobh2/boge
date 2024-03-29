# MQTT setup

first the password part of the config needs to be commented out.

The exec into the container:

```
docker exec -it mqtt sh
```

Then run this

```
mosquitto_passwd -c /mosquitto/config/password.txt sensors
```

exit the container and uncomment the password part of the config and reboot

