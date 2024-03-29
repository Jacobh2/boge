#!/bin/bash

set -e

# Update and Upgrade the Pi, just in case
sudo apt-get update -y && sudo apt-get upgrade -y

# Install nginx
sudo apt-get install nginx -y

# Copy the confs over to /etc/nginx/sites-available
cp boge.conf /etc/nginx/sites-available/boge.conf
cp local.conf /etc/nginx/sites-available/local.conf
cp redirect.conf /etc/nginx/sites-available/redirect.conf

# Enable the new server block by creating a symbolic link
sudo ln -s /etc/nginx/sites-available/boge.conf /etc/nginx/sites-enabled/
sudo ln -s /etc/nginx/sites-available/local.conf /etc/nginx/sites-enabled/
sudo ln -s /etc/nginx/sites-available/redirect.conf /etc/nginx/sites-enabled/

# Test the nginx configuration for syntax errors
sudo nginx -t

# Reload nginx to apply the changes
sudo systemctl reload nginx

echo "Nginx has been installed and configured."
