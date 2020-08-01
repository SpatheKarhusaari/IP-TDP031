#!/usr/bin/env python3

import sys
import pexpect
import os

if __name__ == "__main__":
    if len(sys.argv) == 2:
        username = sys.argv[1]
        


        os.chdir("/var/yp")
        compiling_db = pexpect.spawn("make")
        compiling_db.expect(pexpect.EOF)
        
        restart_services = pexpect.spawn("service nis restart")
        restart_services.expect(pexpect.EOF)
        restart_services.sendline("service autofs restart")
        restart_services.expect(pexpect.EOF)

        print(str(username) + ": REMOVED")