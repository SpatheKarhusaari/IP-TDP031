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
        debug("Setting up, using scp, on " + ip)
        child = pexpect.spawn("scp -r -P 2220 " + setup_files + " root@" + ip + ":~/")
    else:
        debug("Setting up, using scp, on " + ip + " through provided ssh-connection")
        child = ssh_client
        child.sendline("scp -r " + setup_files + " root@" + ip + ":~/")
    child.expect("root@" + ip + "'s password:" or pexpect.TIMEOUT)
    child.sendline("password")

    # Establish ssh, if there is already a connection,
    # establish a new one through the provided one
    if ssh_client == None:
        child.expect(pexpect.EOF or pexpect.TIMEOUT)
        child.close()
        
        debug("Establishing ssh connection to " + ip)
        child = pexpect.spawn("ssh -p 2220 root@" + ip)
    else:
        child.expect("root@.*:~# " or pexpect.TIMEOUT)
        
        debug("Establishing ssh connection to " + ip + " through provided ssh-connection")
        child.sendline("ssh root@" + ip)
    
    child.expect("root@" + ip + "'s password:" or pexpect.TIMEOUT) 
    child.sendline("password")
    child.expect("root@.*:~# " or pexpect.TIMEOUT)
    return child

def test_hostname(ssh_client, hostname):
    # Run check_hostname.py
    ssh_client.sendline("python3 check_hostname.py " + hostname)
    ssh_client.expect("Result:.*"or pexpect.TIMEOUT)
    
    # Parse result
    result = str(ssh_client.after.rstrip().decode("utf-8"))
    debug(" Testing Hostname for \""+ hostname + "\"")
    assert(result == "Result: True")
    debug("     " + result)

def test_ping(ssh_client, ip):
    # Ping provided ip
    ssh_client.sendline("ping -c 1 -W 1 " + ip)
    ssh_client.expect("1 packets transmitted,.*" or pexpect.TIMEOUT)
    
    # Parse result
    result = str(ssh_client.after.rstrip().decode("utf-8"))
    debug("     Test pinging: "+ ip)
    assert(" 0% packet loss" in result)
    debug("         PASSED")

def run_tests(ssh_client, hostname):
    debug("Running tests for: \"" + hostname + "\"")
    test_hostname(ssh_client, hostname)

    debug(" Testing Internal Connectivity")
    test_ping(ssh_client, "10.0.0.1")
    test_ping(ssh_client, "10.0.0.2")
    test_ping(ssh_client, "10.0.0.3")
    test_ping(ssh_client, "10.0.0.4")

    debug(" Testing External Connectivity without name lookup")
    ssh_client.sendline("curl 91.198.174.194") #IP address of wikipedia.com
    ssh_client.expect("</html>" or pexpect.TIMEOUT)
    debug("     PASSED")


    debug(" Testing External Connectivity with name lookup")
    ssh_client.sendline("curl google.com")
    ssh_client.expect("(?:curl: |</HTML>)" or pexpect.TIMEOUT)
    debug("     PASSED\n")

if __name__ == "__main__":
    if len(sys.argv) == 2:
        DEBUG = sys.argv[1].upper() == 'DEBUG'

    # Establish ssh to router and run tests
    ssh_client = establish_ssh_and_setup("127.0.0.1", "check_hostname.py")
    run_tests(ssh_client, "gw")

    # Establish ssh to server and run tests
    ssh_client = establish_ssh_and_setup("10.0.0.2", "check_hostname.py", ssh_client)
    run_tests(ssh_client, "server")
    
    # Cleanup on server and exit back to router
    ssh_client.sendline("rm check_hostname.py")
    ssh_client.sendline("exit")
    ssh_client.expect("root@gw:~# " or pexpect.TIMEOUT)

    # Establish ssh to client-1 and run tests
    ssh_client = establish_ssh_and_setup("10.0.0.3", "check_hostname.py", ssh_client)
    run_tests(ssh_client, "client-1")
    
    # Cleanup on client-1 and exit back to router
    ssh_client.sendline("rm check_hostname.py")
    ssh_client.sendline("exit")
    ssh_client.expect("root@gw:~# " or pexpect.TIMEOUT)

    # Establish ssh to client-2 and run tests
    ssh_client = establish_ssh_and_setup("10.0.0.4", "check_hostname.py", ssh_client)
    run_tests(ssh_client, "client-2")
    
    # Cleanup on client-2 and exit back to router
    ssh_client.sendline("rm check_hostname.py")
    ssh_client.sendline("exit")
    ssh_client.expect("root@gw:~# " or pexpect.TIMEOUT)

    # Cleanup on router
    ssh_client.sendline("rm check_hostname.py")
    ssh_client.sendline("exit")

# End
print("ALL NET TESTS PASSED")
