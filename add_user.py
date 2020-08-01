#!/usr/bin/env python3

import sys
import pexpect
import os

if __name__ == "__main__":
    if len(sys.argv) == 3:
        username = sys.argv[1]
        password = sys.argv[2]

        f = open("/etc/passwd", "r")
        passwd_file = f.read()
        if username in passwd_file: 
            n = 1
            username += str(n)
            while username in passwd_file:
                username = username[:-1]
                username += str(n)
                n += 1
     
        adding_user = pexpect.spawn("useradd -d /home/" + str(username) + " " + str(username))
        adding_user.expect(pexpect.EOF)
        adding_user.sendline("usermod --shell /bin/bash " + str(username))
        adding_user.expect(pexpect.EOF)

        changing_password = pexpect.spawn("passwd " + str(username))
        changing_password.expect("New password: ")
        changing_password.sendline(password)
        changing_password.expect("Retype new password: ")
        changing_password.sendline(password)
        changing_password.expect("passwd: password updated successfully")
        
        creating_homedir = pexpect.spawn("mkdir /home1/" + str(username))
        creating_homedir.expect(pexpect.EOF)

        readme_f = open("/home1/"+ str(username)+"/README.txt", "w+")
        readme_f.write("Welcome " + str(username) + "! Hello World to you!\n")
        readme_f.close()
        
        fixing_permissions = pexpect.spawn("chown " + str(username) + " -R /home1/" + str(username))
        fixing_permissions.expect(pexpect.EOF)
        fixing_permissions.sendline("chmod -R 700 /home1/" + str(username))
        fixing_permissions.expect(pexpect.EOF)

        auto_home_f = open("/etc/auto.home", "a+")
        auto_home_f.write(str(username) + " -fstype=nfs,rw 10.0.0.2:/home1/" + str(username) + "\n")
        auto_home_f.close()
        
        os.chdir("/var/yp")
        compiling_db = pexpect.spawn("make")
        compiling_db.expect(pexpect.EOF)
        
        restart_services = pexpect.spawn("service nis restart")
        restart_services.expect(pexpect.EOF)
        restart_services.sendline("service autofs restart")
        restart_services.expect(pexpect.EOF)

        print(str(username) + ": ADDED")

    elif len(sys.argv) > 3:
        print("Too many Arguments, Usage: add_user.py USERNAME PASSWORD")
    else:
        print("Missing Arguments, Usage: add_user.py USERNAME PASSWORD")
        
