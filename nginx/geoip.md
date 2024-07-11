# Geo

only allow swedes

1. wget https://cdn.jsdelivr.net/npm/geolite2-country@1.0.2/GeoLite2-Country.mmdb.gz
2. gzip -d GeoLite2-Country.mmdb.gz
3. sudo mkdir -p /usr/share/GeoIP/
4. sudo mv GeoLite2-Country.mmdb /usr/share/GeoIP/
5. sudo apt install nginx-full
6. Add to http section of nginx (`/etc/nginx/nginx.conf`)

    ```
    geoip2 /usr/share/GeoIP/GeoLite2-Country.mmdb {
        auto_reload 5m;
        $geoip2_data_country_code country iso_code;
    }
    ```

7. Add before all "location" parts in server

    ```
    if ($geoip2_data_country_code != 'SE') {
        return 403;
    }
    ```
