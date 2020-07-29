# NIS
## Qs and As
Can be found on drive, NOT DONE
## Setup

### ALL

```
Run these commands on all machines before proceeding : 
apt install ntp
apt install ntpstat #for tests
apt install ntpdate #for tests
```

### GW/Router
```IP: 10.0.0.1```

* START HERE! Server installation
    * Install NTP - "apt install ntp"
    * Update the newly created /etc/ntp.conf with the below file
        * This makes this machine into a NTP server
    * Restart machine/service - "shutdown -r 0/service ntp restart"
    * Verify that everything worked by running - "service ntp status"
* [/etc/ntp.conf](../3-NTP/gw/etc/ntp.conf)

### server
```IP: 10.0.0.2```

* Client installation
    * Update /etc/hosts with the below file
        * This adds gw as a host
    * Verify that client is synced with "ntpdate 10.0.0.1"
    * Turn off the pesky systemd timesyncd by running "timedatectl set-ntp off"
        * This is the automatic NTP which will interfere with our own if not disabled
    * Install NTP - "apt install ntp" 
    * Update /etc/ntp.conf with the below file
        * This adds gw as the NTP server to use
    * Finally restart the ntp service - "service ntp restart"
    * Repeat with appropriate files on other clients
* [/etc/hosts](../3-NTP/server/etc/hosts)
* [/etc/ntp.conf](../3-NTP/server/etc/ntp.conf)

### client-1
```IP: 10.0.0.3```

* [/etc/hosts](../3-NTP/client-1/etc/hosts)
* [/etc/ntp.conf](../3-NTP/client-1/etc/ntp.conf)

### client-2
```IP: 10.0.0.4```

* [/etc/hosts](../3-NTP/client-2/etc/hosts)
* [/etc/ntp.conf](../3-NTP/client-2/etc/ntp.conf)

## Tests
* [/tests/check_time_sync.py](../3-NTP/tests/check_time_sync.py)
    * Has to be ran on each individual machine. 
    * Use start_NTP_tests.py to facilitate this
* [/tests/start_NIS_tests.py](../3-NTP/tests/start_NTP_tests.py)
    * run using `python start_NIS_tests.py [debug]`
    * You have to stand in the tests directory for this to work, no time to fix this