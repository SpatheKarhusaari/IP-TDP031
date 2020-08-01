# NIS
## Qs and As
Can be found on drive, NOT DONE
## Setup

### ALL

```
Run these commands on server, client-1 and client-2 before proceeding : 
apt install ntp

```

### GW/Router
```IP: 10.0.0.1```
* Nothing this time

### server
```IP: 10.0.0.2```

* START HERE
    * install NIS: "apt install NIS"
        * Provide a Domain Name, in our case it is: student.ida.liu.se
    * Replace /etc/default/nis with the below file
        * This will make server into the NIS server
    * Replace /etc/ypserv.securenets with the below file
        * This is done to restrict access to only our subnet instead of everyone
    * Initialize the NIS server: "/usr/lib/yp/ypinit -m" and press ctrl+ d as the list of NIS servers is already appropriate
    * Replace /etc/yp.conf with the below file
        * Remember to restart service after changing config files
* Create a user
    * Run "useradd -d /home/testuser -m testuser"
    * Run "passwd testuser"
        * Interactive prompt will appear. Give appropriate password
    * Run "cd /var/yp/" 
    * run "make"
        * This recompile the NIS db
    * Finally "ypcat passwd"
        *  This last command is to validate that your configuration works
* [/etc/default/nis](../4-NIS/server/etc/default/nis)
* [/etc/yp.conf](../4-NIS/server/etc/yp.conf)
* [/etc/ypserv.securenets](../4-NIS/server/etc/ypserv.securenets)

### client-1
```IP: 10.0.0.3```
* install NIS: "apt install NIS"
    * Provide a Domain Name, in our case it is: student.ida.liu.se
* Replace /etc/yp.conf with the below file
    * Remember to restart service after changing config files
* Replace /etc/nsswitch.conf with the below file
    * This changes the priority so that while logging in it checks local files, then NIS so that we do not have problems with root being overwritten
* This can be tested by runnig ypcat passwd or trying to ssh into your added test user.
* Repeat on client-2 afterwards

* [/etc/yp.conf](../4-NIS/client-1/etc/yp.conf)
* [/etc/nsswitch.nsswitch](../4-NIS/client-1/etc/nsswitch.conf)

### client-2
```IP: 10.0.0.4```

* [/etc/yp.conf](../4-NIS/client-2/etc/yp.conf)
* [/etc/nsswitch.conf](../4-NIS/client-2/etc/nsswitch.conf)

## Tests
* [/tests/check_time_sync.py](../4-NIS/tests/check_NIS_config.py)
    * Has to be ran on each individual machine. 
    * Use start_NTP_tests.py to facilitate this
* [/tests/start_NIS_tests.py](../4-NIS/tests/start_NIS_tests.py)
    * run using `python start_NIS_tests.py [debug]`
    * You have to stand in the tests directory for this to work, no time to fix this