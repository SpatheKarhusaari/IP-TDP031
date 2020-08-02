#!/usr/bin/env python3

# Has to be ran on server

import sys
import pexpect
import os

if __name__ == "__main__":
    if len(sys.argv) == 2:
        username = sys.argv[1]
        
        f = open("/etc/passwd", "r")
        passwd_file = f.read()    
        if str(username) + ":" in passwd_file:

            removing_dir = pexpect.spawn("rm -rf /home1/" + str(username))
            removing_dir.expect(pexpect.EOF)

            removing_user = pexpect.spawn("userdel " + str(username))
            removing_user.expect(pexpect.EOF)

            auto_home_f = open("/etc/auto.home", "r")

            new_auto_home_content = ""

            for line in auto_home_f:
                #Ignore comments
                if line[0] == "#":
                    new_auto_home_content += line
                    continue

                if str(username) + " " not in line:
                    new_auto_home_content += line

            auto_home_f.close()
            auto_home_f = open("/etc/auto.home", "w")
            auto_home_f.write(new_auto_home_content)

            os.chdir("/var/yp")
            compiling_db = pexpect.spawn("make")
            compiling_db.expect(pexpect.EOF)
            
            restart_services = pexpect.spawn("service nis restart")
            restart_services.expect(pexpect.EOF)
            restart_services.sendline("service autofs restart")
            restart_services.expect(pexpect.EOF)

            print("\""+ str(username) + "\": REMOVED")
        else:
            print("User: \"" + str(username) + "\" does not exist!")
    
    elif len(sys.argv) > 2:
        print("Too many Arguments, Usage: cleanup_user.py USERNAME")
    else:
        print("Missing Arguments, Usage: cleanup_user.py USERNAME")