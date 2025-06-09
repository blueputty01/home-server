sudo cryptsetup open /dev/sda1 extension --type luks
sudo mount /dev/mapper/extension /mnt/extension

sudo cryptsetup open /dev/sdb backup --type luks
sudo mount /dev/mapper/backup /mnt/backup
