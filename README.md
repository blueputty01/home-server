# Architecture

Multi-container stacks run on Docker compose and deployed privately via tailscale.


# Features

- Anki (custom Docker image)
- Budgeting system (Actual)
- Gitea
- Home Assistant
- Immich
- Opencloud
- Youtrack

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
