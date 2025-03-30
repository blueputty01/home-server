# Architecture

Built on docker compose and deployed privately via tailscale.

Extend `tailscale.yaml` in the root directory and specify `hostname` to automatically add the subdomain for the stack to the tailnet.

Ephemeral containers disabled in case containers temporarily lose connection.

# Features

Refer to README under each stack for detailed operation information.

## Photos

Uses [immich](https://immich.app/)

## Anki

## Budget

Uses [Actual](https://github.com/actualbudget/actual-server)

## Smart home

Uses [ESPHome](https://esphome.io/guides/getting_started_command_line)

## Backup

```bash
borg init --encryption repokey-blake2 ~/docker-data
```
## Nextcloud 

[Nextcloud AIO](https://github.com/nextcloud/all-in-one#nextcloud-all-in-one)

Note that the containers might not be able resolve the nextcloud domain due to ACL policies on the Tailscale admin console 

[Tailscale Reverse Proxy setup](https://github.com/nextcloud/all-in-one/discussions/5439)

# Development

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
