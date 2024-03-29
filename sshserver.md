# SSH Server

The purpose of the SSH server is to:

- Handle the termination of SSL and domain
- Have a ssh server running on port 22

## Requireemnts

- nginx
    - Usually installed by default, but make sure & upgrade to latest version
- sshserver
    - Usually setup when flashing the sd card
- Boge needs to be allowed to ssh!
    add the public key to the 'authorized_keys' file
- proxy_tunnle.service service that connects back to boge
    - follow steps in onboot.md file.
    - sshserver should have the scripts/start_tunnle.sh script
    
