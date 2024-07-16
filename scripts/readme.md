# Scripts


## sshserver

ssh server should have the `start_tunnle.sh` script to setup the connection
on port 8123 from sshserver -> boge via localhost on the already setup tunnle.


## boge

Boge will connect to sshserver using the domain.

### Version 2

The second version, `start_tunnle_remote_2.sh`, includes a check of the logs from ssh to identify a faulty connection and then automatically kill the process and restart. We test this since we have seen in the logs that the connection dies after some time with this in the logs:

```
Jul 12 00:01:34 boge start_tunnle.sh[4744]: debug1: remote forward failure for: listen <localport>, connect 0.0.0.0:<ssh-port>
Jul 12 00:01:34 boge start_tunnle.sh[4744]: Warning: remote port forwarding failed for listen port <localport>
```

## ssh keys

the ssh server needs a private key th

### Read logs from services



