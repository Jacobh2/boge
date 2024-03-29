# Nginx config

## Install

Use the install.sh script and the prepare.sh script

##

the ssh server is responsible for terminating SSL. This is done since it is the one the domain points to.

Config is found in `nginx/*.conf` files.

On the server this is located at 

```
/etc/nginx/sites-available/boge.conf
/etc/nginx/sites-available/redirect.conf
```


## Generate basic auth file

```bash
htpasswd -nb username password
```

## Reload nginx config

```bash
/etc/init.d/nginx reload
```

## Verify nginx config

```bash
sudo nginx -t
```

## Activate site

```bash
ln -s /etc/nginx/sites-available/www.example.org.conf /etc/nginx/sites-enabled/
```

## To map multiple ports:


