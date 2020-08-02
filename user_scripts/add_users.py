#!/usr/bin/env python3

import pexpect

def add_user(username, password, ssh_client):
    ssh_client.sendline("python3 add_user.py " + str(username) + " " + str(password))
    ssh_client.expect("\".*\": ADDED")
    return str(ssh_client.after.rstrip().decode('utf-8')).split(":")[0]

def establish_ssh():
    #Establishing SSH to router
    ssh_client = pexpect.spawn("ssh root@127.0.0.1 -p 2220")
    ssh_client.expect("root@127.0.0.1\'s password:" or pexpect.TIMEOUT)
    ssh_client.sendline("password")
    ssh_client.expect("root@.*:~# " or pexpect.TIMEOUT)

    #Establishing SSH to server
    ssh_client.sendline("ssh root@server")
    ssh_client.expect("root@server's password:" or pexpect.TIMEOUT)
    ssh_client.sendline("password")
    ssh_client.expect("root@.*:~# " or pexpect.TIMEOUT)

    return ssh_client

if __name__ == "__main__":
    print("Welcome to the Domain User Utility!")
    print("Setting up connection to server!")
    ssh_client = establish_ssh()
    
    username = input("What is the username you would like to add: ")
    password = input("and what password should " + str(username) + " have: ")
    
    actual_username = add_user(username, password, ssh_client)
    print("##### User: " + actual_username + " added! #####")
    
    ssh_client.close()
    print("Domain User Utility finishing up!")
    
