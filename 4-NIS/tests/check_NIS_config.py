#!/usr/bin/env python3

import pexpect
import socket

if __name__ == "__main__":
    # Testing that the correct server is used
    child = pexpect.spawn("ypwhich")
    child.expect(["server.student.ida.liu.se", "localhost"] or pexpect.TIMEOUT)
    if socket.gethostname() == "server":
        assert(str(child.after.rstrip().decode("utf-8")) == "localhost")
    else:
        assert(str(child.after.rstrip().decode("utf-8")) == "server.student.ida.liu.se")
    
    # Testing whether we have a connecton to server
    # Also tests whether there is a NIS only user
    child = pexpect.spawn("ypcat passwd")
    child.expect("testuser" or pexpect.TIMEOUT)
    
    #END
    print("PASSED")

        

