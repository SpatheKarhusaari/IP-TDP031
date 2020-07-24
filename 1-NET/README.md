# NET
## Qs and As
Can be found on drive, NOT DONE
## Setup
### GW/Router
```
IP: 10.0.0.1
```
* [/etc/network/interfaces](../1-NET/gw/etc/network/interfaces)
    * ifdown/ifup doesn't work for me, restart of system required after changes to interfaces
    * Added an interface for ens4 with the above IP
* [/etc/hostname](../1-NET/gw/etc/hostname)
* [/etc/hosts](../1-NET/gw/etc/hosts)
* [/etc/rc.local](../1-NET/gw/etc/rc.local)
    * NEEDS EXPLANATION
* [/etc/resolv.conf](../1-NET/gw/etc/resolv.conf)
    * IP is taken from instructions
* [/etc/sysctl.conf](../1-NET/gw/etc/sysctl.conf)
    * remove # from the line containing: `net.ipv4.ip_forward=1`
* [/proc/sys/net/ipv4/ip_forward](../1-NET/gw/proc/sys/net/ipv4/ip_forward)
    * created through the command on the course page. Does no persists through reboot. Use the above setup instead

### server
```
IP: 10.0.0.2
```
* [/etc/network/interfaces](../1-NET/server/etc/network/interfaces)
* [/etc/hostname](../1-NET/server/etc/hostname)
* [/etc/hosts](../1-NET/server/etc/hosts)
* [/etc/resolv.conf](../1-NET/server/etc/resolv.conf)

### client-1
```
IP: 10.0.0.3
```
* [/etc/network/interfaces](../1-NET/client-1/etc/network/interfaces)
* [/etc/hostname](../1-NET/client-1/etc/hostname)
* [/etc/hosts](../1-NET/client-1/etc/hosts)
* [/etc/resolv.conf](../1-NET/client-1/etc/resolv.conf)

### client-2
```
IP: 10.0.0.4
```
* [/etc/network/interfaces](../1-NET/client-2/etc/network/interfaces)
* [/etc/hostname](../1-NET/client-2/etc/hostname)
* [/etc/hosts](../1-NET/client-2/etc/hosts)
* [/etc/resolv.conf](../1-NET/client-2/etc/resolv.conf)

## Tests
* [check_hostname.py](../1-NET/tests/check_hostname.py)
    * run using `python check_hostname.py CORRECT_HOSTNAME`
    * Needs to be deployed to the machine being tested. Use start_NET_tests.py to facilitate this

* [start_NET_tests.py](../1-NET/tests/start_NET_tests.py)
    * run using `python start_NET_tests.py [debug]`
    * You have to stand in the tests directory for this to work, no time to fix this