#!/usr/bin/env python3

# Breaking: run "systemctl stop bind9" on server

import pexpect
import sys
import socket 

if __name__ == "__main__":
    hostname = socket.gethostname()

    # Authoritative answer from local DNS with norecourse flag  
    child = pexpect.spawn("dig +norecurse +short @10.0.0.2 gw.student.ida.liu.se")
    child.expect("10.0.0.1" or pexpect.TIMEOUT)
    
    child = pexpect.spawn("dig +norecurse +short @10.0.0.2 server.student.ida.liu.se")
    child.expect("10.0.0.2" or pexpect.TIMEOUT)
    
    child = pexpect.spawn("dig +norecurse +short @10.0.0.2 client-1.student.ida.liu.se")
    child.expect("10.0.0.3" or pexpect.TIMEOUT)

    child = pexpect.spawn("dig +norecurse +short @10.0.0.2 client-2.student.ida.liu.se")
    child.expect("10.0.0.4" or pexpect.TIMEOUT)

    # Recursive answer from local DNS
    child = pexpect.spawn("dig +short @10.0.0.2 google.com")
    child.expect("\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}" or pexpect.TIMEOUT)
    
    child = pexpect.spawn("dig +short @10.0.0.2 wikipedia.com")
    child.expect("\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}" or pexpect.TIMEOUT)

    # Reverse zone requests
    child = pexpect.spawn("dig +short @10.0.0.2 -x 10.0.0.1")
    child.expect("gw.student.ida.liu.se")

    child = pexpect.spawn("dig +short @10.0.0.2 -x 10.0.0.2")
    child.expect("server.student.ida.liu.se")
    
    child = pexpect.spawn("dig +short @10.0.0.2 -x 10.0.0.3")
    child.expect("client-1.student.ida.liu.se")
    
    child = pexpect.spawn("dig +short @10.0.0.2 -x 10.0.0.4")
    child.expect("client-2.student.ida.liu.se")

    # Internal Pings without IPs
    child = pexpect.spawn("ping -c 1 -W 1 gw.student.ida.liu.se")
    child.expect("1 packets transmitted,.*" or pexpect.TIMEOUT)

    # Parse result
    result = str(child.after.rstrip().decode("utf-8"))
    assert(" 0% packet loss" in result)
    print("END")

