# Features

Multi-container stacks running on Docker compose.

## Applications

In rough order of personal importance:

| Application | Description |
| :--- | :--- |
| Immich | Cloud photos |
| Opencloud | Cloud file storage |
| Paperless | Digital document archive |
| Youtrack | Project management |
| Home Assistant | Mic/speaker, voice synthesis, automatic speech recognition, and central automation containers |
| ESPHome | Flash custom firmware to smart home devices |
| Open WebUI | Extensible self-hosted AI platform |
| Yamtrack | Book tracking |
| Actual | Budgeting system |
| Gitea | Git service |
| Anki | Custom Docker image exposing sync server |
| System | Custom C++ dashboard for system monitoring |

Tailscale is used to expose applications via VPN to only trusted clients through convenient, secured paths like `https://photos.tailxxxxxx.ts.net/`

## Active development

- Container orchestration for home assistant to offload speech recognition to more capable hardware in the system
- OIDC integration across the system for centralized user management

# System configuration

## Backup

This project currently uses a script to backup the Docker volumes and configuration files (.env, etc). I am exploring migrating this to a docker container to containerize the [Borg](https://borgbackup.readthedocs.io/en/stable/quickstart.html) dependency.

But currently, the best way to enable backup is to ensure python and Borg are installed and run the job:

```
0 4 * * 1 /home/alex/home-server/scripts/backup.sh
```

## Security

Ports published by Docker containers are publicly accessible even if UFW rules would normally block them! I'm currently applying [this](https://github.com/chaifeng/ufw-docker) guide to lock down the host.

## Development

### Tailscale configuration

Extend `tailscale.yaml` in the root directory and specify `hostname` to automatically add the subdomain for the stack to the tailnet.

Ephemeral containers disabled in case containers temporarily lose connection.

### File structure

This project uses a combination of [git subtree](https://www.atlassian.com/git/tutorials/git-subtree) and git submodules. Generally, if the external project is externally owned, git subtree will be used, otherwise git submodules will be used. The needed git subtree commands are below.

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
