sudo cryptsetup open 98f868d6-3a25-476c-b34f-ced4c5b6f9b2 extension --type luks
sudo mount /dev/mapper/extension /mnt/extension

sudo cryptsetup open 121874b8-4873-446d-bbc9-5e83eb69a35f backup --type luks
sudo mount /dev/mapper/backup /mnt/backup
