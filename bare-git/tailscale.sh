#!/bin/sh

su git
cd /home/git
git init --bare obsidian-default
su root

tailscaled --statedir=/var/lib/tailscale --tun=userspace-networking &
tailscale up --ssh --auth-key="${TS_AUTHKEY}" --hostname=git ${TS_EXTRA_ARGS}

wait

exec "$@"
