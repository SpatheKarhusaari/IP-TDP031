#!/usr/bin/env python3
import os
import sys

if __name__ == "__main__":
    print()
    DEBUG = "d"
    if len(sys.argv) == 2:
        if sys.argv[1].upper() == "DEBUG": 
            DEBUG = "DEBUG"
    
    print("Executing Test Suite! This might take some time")

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
    os.chdir("3-NTP/tests")
    os.system("python3 start_NTP_tests.py " + DEBUG + " ") # Add: + " breaking" to run with all tests
    os.chdir("../../")
    print("##################################################\n") 

    # NIS tests
    os.chdir("4-NIS/tests")
    os.system("python3 start_NIS_tests.py " + DEBUG)
    os.chdir("../../")
    print("##################################################\n") 

    # STO tests
    print("No Tests implemented for STO")
    print("##################################################\n") 
    
    # NFS tests
    os.chdir("6-NFS/tests")
    os.system("python3 start_NFS_tests.py " + DEBUG)
    os.chdir("../../")
    print("##################################################\n") 
