# SSD Connection

This flowchart shows how the SSH connections are being made


```mermaid
flowchart LR
    
    subgraph "boge"
        boge_http[HTTP]
        boge_ssh[ssh]

        boge_ssh -.-> boge_http
    end

    subgraph "sshserver"
        sshserver_http[HTTP]
        sshserver_ssh[ssh]

        sshserver_http -.->sshserver_ssh
    end


    domain[domain]

    internet[Internet]

    boge_ssh --9091-->  sshserver_ssh
    sshserver_ssh --8080--> boge_ssh

    domain --80--> sshserver_http

    internet --> domain


```

## From Boge

During boot, Boge does the following:

1. Check if we can resolve the domain
2. Once the domain is resolved, we know we have internet, continue
3. Connect to domain on port defined in router, map that to 9091 on target

## From SSH Server

During boot, the SSH Server does the following:

1. Connect to localhost on port 9091, map connection from port 80 to port 8080

## Check service status:

**Boge:**

```sh
systemctl status ssh_reverse_proxy.service
````

**SSH Server:**

proxy tunnle
```sh
systemctl status proxy_tunnle.service
````

nginx
```sh
systemctl status nginx
````