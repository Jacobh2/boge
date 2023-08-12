# Nginx config

the ssh server is responsible for terminating SSL. This is done since it is the one the domain points to.

Config is found in `nginx/nginx.conf` file


## Generate basic auth file

```bash
htpasswd -nb username password
```