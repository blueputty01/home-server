#!/bin/bash

sudo nft add table ip filter
sudo nft add chain ip filter forward { type filter hook forward priority 0; }
sudo nft add rule ip filter forward iifname "traefik0" oifname "frontend0" accept

sudo nft list ruleset > /etc/nftables.conf
