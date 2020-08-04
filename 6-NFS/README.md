# NFS
## Qs and As
Can be found on drive, NOT DONE
## Setup

### GW/Router
```IP: 10.0.0.1```
* Nothing this time

### server
```IP: 10.0.0.2```

* START HERE
* Static Export
    * Run `apt install nfs-kernel-server`
    * Run `chown nobody:nogroup /usr/local`
    * Run `chmod 777 /usr/local`
        * The last 2 is to prepare /usr/local for export to clients
    * Replace /etc/exports with the below file
        * This adds the above directory to exports with rules that are explained in the file
        * Run `exportfs -a`
        * Run `systemctl restart nfs-kernel-server.service`
            * These finalizes the export. Remember to run these AFTER every edit of /etc/exports
    * Continue on clients
* Indirect Export based on login
    * Create 2 new NIS users
        * Run `useradd -d /home/tester1 tester1`
        * Run `useradd -d /home/tester2 tester2`
        * Run `passwd tester1`
        * Run `passwd tester2`
        * Create the folders tester1 and tester2 in their respective home dirs: /home1 and /home2
    * Add these to exports
        * Should have already been done earlier
        * If not replace /etc/exports for the below file
        * Remember to run the above commands after editing /etc/exports
    * Install an automounter on the clients and server. autofs is used here
        * Run `apt install autofs`
    * Configure autofs on server
        * Replace /etc/auto.master with the below file
            * This adds the auto.home map source to autofs
        * Replace /etc/auto.home with the below file
            * This maps the username to the created user directory
        * Add these files to yellow pages and export them
            * Run `cd /var/yp`
            * Run `make auto.master`
                * Compiles the file into the right format
            * Run `make auto.home`
            * Run `cp auto.master student.ida.liu.se/auto.master`
            * Run `cp auto.home student.ida.liu.se/auto.home`
            * Run `service nis restart` 
            * Run `service autofs restart`
    * Continue with configuration on clients
* [/etc/auto.home](../6-NFS/server/etc/auto.home)
* [/etc/auto.master](../6-NFS/server/etc/auto.master)
* [/etc/exports](../6-NFS/server/etc/exports)

### client-1
```IP: 10.0.0.3```

* Static Export
    * Run `apt install nfs-common`
    * Run `mkdir -p /mnt/usr/local`
        * Creates the mount point for the static export
    * Add the line in the below file to /etc/fstab
        * DO NOT REPLACE /etc/fstab with the below file. The rest of fstab is crucial for the vm to work 
* Indirect export based on login
    * Install an automounter
        * Run `apt install autofs`
    * Configure autofs on clients
        * Replace /etc/nsswitch.conf with the below file
* At this point you should be able to log in with one of the above NIS users and have a synced home directory exported from the server
* [/etc/fstab](../6-NFS/client-1/etc/fstab)
* [/etc/exports](../6-NFS/client-1/etc/nsswitch.conf)


### client-2
```IP: 10.0.0.4```

* Static Export
    * Run `apt install nfs-common`
    * Run `mkdir -p /mnt/usr/local`
        * Creates the mount point for the static export
    * Add the line in the below file to /etc/fstab
        * DO NOT REPLACE /etc/fstab with the below file. The rest of fstab is crucial for the vm to work 
* Indirect export based on login
    * Install an automounter
        * Run `apt install autofs`
    * Configure autofs on clients
        * Replace /etc/nsswitch.conf with the below file
* At this point you should be able to log in with one of the above NIS users and have a synced home directory exported from the server
* [/etc/fstab](../6-NFS/client-1/etc/fstab)
* [/etc/exports](../6-NFS/client-2/etc/nsswitch.conf)

## Tests
* [/tests/start_NFS_tests.py](../6-NFS/tests/start_NFS_tests.py)
    * run using `python start_NFS_tests.py [debug]`
    * You have to stand in the tests directory for this to work, no time to fix this

## Adding a user
A script to add a user to the domain has been created. It is ran by `python3 /user_scripts/add_users.py`