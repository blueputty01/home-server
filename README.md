



# Features


Multi-container stacks running on Docker compose.


Applications:


- Anki (custom Docker image exposing sync server)
- Actual (budgeting system)
- Gitea (git server and frontend)
- Home Assistant: mic/speaker, voice synthesis, automatic speech recognition, and central automation containers
- Immich (cloud photos)
- Opencloud (cloud file storage)
- Youtrack (project management)


Tailscale is used to expose applications (via VPN) only to trusted clients through convenient domains like https://photos.tailxxxxxx.ts.net/


# Backup


Edit root crontab:


```
0 4 * * 1 /home/alex/home-server/scripts/backup.sh
```


# Development


Extend `tailscale.yaml` in the root directory and specify `hostname` to automatically add the subdomain for the stack to the tailnet.


Ephemeral containers disabled in case containers temporarily lose connection.




## System configuration


https://github.com/chaifeng/ufw-docker


## Subtree


This project uses [git subtree](https://www.atlassian.com/git/tutorials/git-subtree). 


Add subtree to remote


```bash
git remote add -f 'remote-alias' 'remote-url'
```


Add subtree




```bash
git subtree add --prefix 'local-path' 'remote-alias' branch --squash
```
Update subtree


```bash
git fetch 'remote-alias' 'branch'
git subtree pull --prefix 'local-path' 'remote-alias' 'branch' --squash
```
