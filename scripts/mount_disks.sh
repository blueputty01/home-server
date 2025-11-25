sudo cryptsetup open /dev/sdb1 extension --type luks
sudo mount /dev/mapper/extension /mnt/extension

sudo cryptsetup open /dev/sdc backup --type luks
sudo mount /dev/mapper/backup /mnt/backup
