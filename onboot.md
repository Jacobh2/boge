1. create script

2. sudo nano /etc/systemd/system/my_service.service

3. setup rule

This is called `ssh_reverse_proxy.service` on Boge

```bash
[Unit]
Description=Open a reverse proxy for SSH
After=network.target

[Service]
ExecStart=/home/jacobhagstedt/start_tunnle.sh
Restart=always
User=jacobhagstedt

[Install]
WantedBy=multi-user.target
```

4. sudo systemctl enable my_service.service

5. sudo systemctl start my_service.service

## Disable a service 

sudo systemctl stop my_service.service
sudo systemctl disable my_service.service