# STO
## Qs and As
Can be found on drive, NOT DONE
## Setup

### GW/Router
```IP: 10.0.0.1```

* Nothing this time

### server
```IP: 10.0.0.2```

* START HERE
    * Install mdadm - "apt install mdadm"
    * Install lvm2 - "apt install lvm2"
    * Start lvm2 - "service lvm2 start"
        * Fungerade inte för mig då det skapas en symlink som service, när man sedan försöker starta den så är linux confat så att om serice filen är tom (en symlink är 0 bytes) så är den "masked" kör "/etc/init.d/lvm2 start" istället.
    * /home1
        * "mdadm --create /dev/md0 --level=raid1 --raid-devices=2 /dev/vda /dev/vdb" - För att skapa en raid1 mellan redan existerande virtuella enheter: "vda" och "vdb"
        * "mkfs -b 1024 /dev/md0" - Formatera ett filsystem på den nya enheten, detta är optimerat för filer av storlek 1KB aka "smaller files"
        * "mkdir /home1"
        * "mount /dev/md0 /home1" - Peka var enheten ska spara sina filer. Detta är dock inte boot persistent. 
        * Boot persistence
            * "blkid" - hitta md0 och kopiera UUID. 
            * Lägg till en rad i /etc/fstab med "UUID=\[ditt_uuid\]    /home1    ext2". Alltså UUID=    mount_point    filsystem
    * /home2
        * "pvcreate /dev/vdc" - Skapa en virtuell device
        * "pvcreate /dev/vdd" - Skapa en virtuell device
        * "vgcreate vg1 /dev/vdc /dev/vdd --physicalextentsize 10MB" - Skapa en virtuell grupp för de 2 virtella enheterna
        * "lvcreate -n lvol0 -L 80MB vg1" - Skapa en logisk volym
        * "mkfs -b 4096 /dev/vg1/lvol0" - Formatera ett filsystem optimerat för 4mb aka "stora filer"
        * "mkdir /home2"
        * "mount /dev/vg1/lvol0 /home2" - Peka var enheten ska spara sina filer. Detta är dock inte boot persistent. 
        * Boot persistence
            * "blkid" - hitta "/dev/mapper/vg1-lvol0 och kopiera UUID. 
            * Lägg till en rad i /etc/fstab med "UUID=\[ditt_uuid\]    /home2    ext2"
* See [here](https://www.digitalocean.com/community/tutorials/how-to-create-raid-arrays-with-mdadm-on-ubuntu-16-04) for a more detailed explanation of mdadm
* See [here](https://www.tecmint.com/create-lvm-storage-in-linux/) for a more detailed explanation of lvm2


### client-1
```IP: 10.0.0.3```

* Nothing this time

### client-2
```IP: 10.0.0.4```

* Nothing this time

## Tests

* Nothing this time