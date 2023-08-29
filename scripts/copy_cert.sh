#!/bin/bash

echo "Copying cert..."
mv key.pem /etc/letsencrypt/live/<domain>/privkey.pem
mv cert.pem /etc/letsencrypt/live/<domain>/fullchain.pem
echo "done. Reloading nginx"
/etc/init.d/nginx reload