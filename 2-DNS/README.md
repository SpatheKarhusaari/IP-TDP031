# DNS
## Qs and As
Can be found on drive, NOT DONE
## Setup
### GW/Router
```IP: 10.0.0.1```

* [/etc/hosts](../2-DNS/gw/etc/hosts)
    * Remember to fix permissions, 644 works!
* [/etc/resolv.conf](../2-DNS/gw/etc/resolv.conf)
    * Remember to fix permissions, 644 works!
    * Also remember to remove/readd immutability for this file, use chattr +/-i /etc/resolv.conf

### server
```IP: 10.0.0.2```

* START HERE!
    * Install Bind9!
    * Name of Package is Bind9, but is mostly referred to as "named"
* [/etc/resolv.conf](../2-DNS/server/etc/resolv.conf)
* [/etc/bind/named.conf.local](../2-DNS/server/etc/bind/named.conf.local)
    * Remember to fix permissions, 644 works!
* [/etc/bind/named.conf.options](../2-DNS/server/etc/bind/named.conf.options)
    * Remember to fix permissions, 644 works!  
* [/etc/bind/fwd.student.ida.liu.se.db](../2-DNS/server/etc/bind/fwd.student.ida.liu.se.db)  
    * Remember to fix permissions, 644 works!  
    * See https://help.ubuntu.com/community/BIND9ServerHowto for an explanation
* [/etc/bind/rev.0.0.10.in-addr.arpa.db](../2-DNS/server/etc/bind/rev.0.0.10.in-addr.arpa.db)  
    * Remember to fix permissions, 644 works!  
    * See https://help.ubuntu.com/community/BIND9ServerHowto for an explanation
       
### client-1
```IP: 10.0.0.3```

* [/etc/hosts](../2-DNS/client-1/etc/hosts)
* [/etc/resolv.conf](../2-DNS/client-1/etc/resolv.conf)

### client-2
```IP: 10.0.0.4```

* [/etc/hosts](../2-DNS/client-2/etc/hosts)
* [/etc/resolv.conf](../2-DNS/client-2/etc/resolv.conf)

## Tests
* Install pip3 on all machines - "sudo apt install python3-pip"
    * Then install the "pexpect" module
* Install dnsutils using "apt install dnsutils" on all machines but server
* [/tests/check_connectivity.py](../2-DNS/tests/check_connectivity.py)
    * Has to be ran on each individual machine. 
    * Use start_DNS_tests.py to facilitate this
* [/tests/start_DNS_tests.py](../2-DNS/tests/start_DNS_tests.py)
    * run using `python start_DNS_tests.py [debug]`
    * You have to stand in the tests directory for this to work, no time to fix this