#!/usr/bin/env python3

import sys
import pexpect
import os

DEBUG = False
def debug(to_print):
    if DEBUG:
        print(" DEBUG: " + to_print)

def establish_ssh(user, ip, ssh_client = None):
    #Establishing SSH to router
    if ssh_client == None:
        debug(" Establishing ssh connection to " + user + "@" + ip)
        ssh_client = pexpect.spawn("ssh "+ user +"@" + ip + " -p 2220")
    else:
        debug(" Establishing ssh connection to " + user + "@" + ip + " through provided client")
        ssh_client.sendline("ssh "+ user +"@" + ip)

    ssh_client.expect(user + "@" + ip + "\'s password:" or pexpect.TIMEOUT)
    ssh_client.sendline("password")
    ssh_client.expect(user + "@.*:~. " or pexpect.TIMEOUT)

    debug("     DONE")
    return ssh_client

def check_exports(ssh_client):
    debug("     Running showmount -e 10.0.0.2")
    ssh_client.sendline("showmount -e 10.0.0.2")
    ssh_client.expect("root@.*:~#" or pexpect.TIMEOUT)
    output = str(ssh_client.before.decode('utf-8'))

    
    debug("         Checking whether /usr/local is exported correctly")
    assert("/usr/local 10.0.0.4,10.0.0.3" in output)
    debug("             PASSED")

    debug("         Checking whether /home1 is exported correctly")
    #Checking whether /home1 is exported correctly
    assert("/home1     10.0.0.4,10.0.0.3" in output)
    debug("             PASSED")

    debug("         Checking whether /home2 is exported correctly")
    #Checking whether /home2 is exported correctly
    assert("/home2     10.0.0.4,10.0.0.3" in output)
    debug("             PASSED")

def check_static_mnt(ssh_client):
    debug("     Running ls /mnt/usr/local")
    ssh_client.sendline("ls /mnt/usr/local")
    ssh_client.expect("root@.*:~# " or pexpect.TIMEOUT)
    assert(len(ssh_client.before) > 0)
    debug("         PASSED")

def check_permissions(ssh_client, should_fail):
    ssh_client.sendline("cd /home/tester1")
    if should_fail:
        debug("     Running cd /home/tester1 as root")
        ssh_client.expect("Permission denied" or pexpect.TIMEOUT)
        debug("         PASSED - FAILED AS EXPECTED")
    else:
        debug("     Running cd /home/tester1 as tester1")
        ssh_client.expect(".*@.*:~. " or pexpect.TIMEOUT)
        
        # Creating test_file
        ssh_client.sendline("touch test_file")
        ssh_client.expect(".*@.*:~. " or pexpect.TIMEOUT)

        ssh_client.sendline("cd ~/")
        ssh_client.expect(".*@.*:~. " or pexpect.TIMEOUT)
        debug("         PASSED")


if __name__ == "__main__":
    if len(sys.argv) == 2:
        DEBUG = sys.argv[1].upper() == 'DEBUG'

    ssh_client = establish_ssh("root", "127.0.0.1")
    
    #Checking permissions on client-1 as tester1
    ssh_client = establish_ssh("tester1", "10.0.0.3", ssh_client)
    check_permissions(ssh_client, False)
    debug("")

    #Cleaning up ssh_client
    ssh_client.sendline("exit")
    ssh_client.expect("root@.*:~# " or pexpect.TIMEOUT)

    #Checking exports and static mount on client-1 as root
    ssh_client = establish_ssh("root", "10.0.0.3", ssh_client)
    check_exports(ssh_client)

    check_static_mnt(ssh_client)

    check_permissions(ssh_client, True)
    debug("")


    #Cleaning up ssh_client
    ssh_client.sendline("exit")
    ssh_client.expect("root@.*:~# " or pexpect.TIMEOUT)

    #Checking permissions on client-2 as tester2
    ssh_client = establish_ssh("tester1", "10.0.0.4", ssh_client)
    check_permissions(ssh_client, False)
    debug("")

    #Cleaning up ssh_client
    ssh_client.sendline("exit")
    ssh_client.expect("root@.*:~# " or pexpect.TIMEOUT)

    #Checking exports and static mount on client-2 as root 
    ssh_client = establish_ssh("root", "10.0.0.4", ssh_client)
    check_exports(ssh_client)

    check_static_mnt(ssh_client)

    check_permissions(ssh_client, True)
    debug("")

    #Cleaning up ssh_client
    ssh_client.sendline("exit")
    ssh_client.expect("root@.*:~# " or pexpect.TIMEOUT)


    #Checking exports on server

    ssh_client = establish_ssh("root", "10.0.0.2", ssh_client)

    debug("Checking exports on server")
    check_exports(ssh_client)
    debug(" Checking that synced file exists")
    ssh_client.sendline("ls /home1/tester1")
    ssh_client.expect(" test_file " or pexpect.TIMEOUT)
    debug("     PASSED")

    debug(" Removing synced test_file on server\n")
    ssh_client.sendline("rm /home1/tester1/test_file")
    ssh_client.expect("root@.*:~# " or pexpect.TIMEOUT)

    #Cleaning up
    ssh_client.close()

    #END
    print("ALL NFS TESTS PASSED")





