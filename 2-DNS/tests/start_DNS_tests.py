#!/usr/bin/env python3

# Breaking: ifdown ens4 on router, ifdown ens3 on any other vm

import pexpect
import sys

DEBUG = False

def debug(to_print):
    if DEBUG:
        print(" DEBUG: " + to_print)

def establish_ssh_and_setup(ip, setup_files, ssh_client = None):
    # Copy the needed files
    # If provided with a already set up ssh connection,
    # Copy the needed files through the provided connection.
    if ssh_client == None:
        debug(" Setting up, using scp, on " + ip)
        child = pexpect.spawn("scp -r -P 2220 " + setup_files + " root@" + ip + ":~/")
    else:
        debug(" Setting up, using scp, on " + ip + " through provided ssh-connection")
        child = ssh_client
        child.sendline("scp -r " + setup_files + " root@" + ip + ":~/")
    child.expect("root@" + ip + "'s password:" or pexpect.TIMEOUT)
    child.sendline("password")

    # Establish ssh, if there is already a connection,
    # establish a new one through the provided one
    if ssh_client == None:
        child.expect(pexpect.EOF or pexpect.TIMEOUT)
        child.close()
        
        debug(" Establishing ssh connection to " + ip)
        child = pexpect.spawn("ssh -p 2220 root@" + ip)
    else:
        child.expect("root@.*:~# " or pexpect.TIMEOUT)
        
        debug(" Establishing ssh connection to " + ip + " through provided ssh-connection")
        child.sendline("ssh root@" + ip)
    
    child.expect("root@" + ip + "'s password:" or pexpect.TIMEOUT) 
    child.sendline("password")
    child.expect("root@.*:~# " or pexpect.TIMEOUT)
    return child

if __name__ == "__main__":
    if len(sys.argv) == 2:
        DEBUG = sys.argv[1].upper() == 'DEBUG'

    # Establish ssh to router and run tests
    debug("Running Tests for gw")
    ssh_client = establish_ssh_and_setup("127.0.0.1", "check_connectivity.py")
    debug("     Running test: \"check_connectivity.py\"")
    ssh_client.sendline("python3 check_connectivity.py")
    ssh_client.expect("PASSED" or pexpect.TIMEOUT)
    debug("PASSED\n")
    
    # Establish ssh to server and run tests
    debug("Running Tests for server")
    ssh_client = establish_ssh_and_setup("10.0.0.2", "check_connectivity.py", ssh_client)
    debug("     Running test: \"check_connectivity.py\"")
    ssh_client.sendline("python3 check_connectivity.py")
    ssh_client.expect("PASSED" or pexpect.TIMEOUT)
    debug("PASSED\n")

    # Cleanup on server and exit back to router
    ssh_client.sendline("rm check_connectivity.py")
    ssh_client.sendline("exit")
    ssh_client.expect("root@gw:~# " or pexpect.TIMEOUT)

    # Establish ssh to client-1 and run tests
    debug("Running Tests for client-1")
    ssh_client = establish_ssh_and_setup("10.0.0.3", "check_connectivity.py", ssh_client)
    debug("     Running test: \"check_connectivity.py\"")
    ssh_client.sendline("python3 check_connectivity.py")
    ssh_client.expect("PASSED" or pexpect.TIMEOUT)
    debug("PASSED\n")

    # Cleanup on client-1 and exit back to router
    ssh_client.sendline("rm check_connectivity.py")
    ssh_client.sendline("exit")
    ssh_client.expect("root@gw:~# " or pexpect.TIMEOUT)

    # Establish ssh to client-2 and run tests
    debug("Running Tests for client-2")
    ssh_client = establish_ssh_and_setup("10.0.0.4", "check_connectivity.py", ssh_client)
    debug("     Running test: \"check_connectivity.py\"")
    ssh_client.sendline("python3 check_connectivity.py")
    ssh_client.expect("PASSED" or pexpect.TIMEOUT)
    debug("PASSED\n")

    # Cleanup on client-2 and exit back to router
    ssh_client.sendline("rm check_connectivity.py")
    ssh_client.sendline("exit")
    ssh_client.expect("root@gw:~# " or pexpect.TIMEOUT)

    #Router specific test for external recursive
    debug("Running router specific test for external recursive queries")
    debug("     Running test: \"dig -b 10.0.2.15 google.com @10.0.0.2\"")
    ssh_client.sendline("dig -b 10.0.2.15 google.com @10.0.0.2")
    ssh_client.expect("status: REFUSED")
    debug("PASSED\n")

    # Cleanup on router
    ssh_client.sendline("rm check_connectivity.py")
    ssh_client.sendline("exit")

    #END
    print("ALL DNS TESTS PASSED")