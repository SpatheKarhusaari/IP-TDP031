#!/usr/bin/env python3
import os
import sys

if __name__ == "__main__":

    DEBUG = ""
    if len(sys.argv) == 2:
        if sys.argv[1].upper() == "DEBUG": 
            DEBUG = "DEBUG"
    
    # NET tests
    os.chdir("1-NET/tests")
    os.system("python3 start_NET_tests.py " + DEBUG)
    os.chdir("../../")
    print("##################################################\n") 

    # DNS tests
    os.chdir("2-DNS/tests")
    os.system("python3 start_DNS_tests.py " + DEBUG)
    os.chdir("../../")
    print("##################################################\n") 

    # NTP tests
    print("NTP TESTS NOT IMPLEMENTED")
    print("##################################################\n") 

    # NIS tests
    print("NIS TESTS NOT IMPLEMENTED")
    print("##################################################\n") 

    # STO tests
    print("STO TESTS NOT IMPLEMENTED")
    print("##################################################\n") 
    
    # NFS tests
    print("NFS TESTS NOT IMPLEMENTED")
    print("##################################################\n") 