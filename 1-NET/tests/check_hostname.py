#!/usr/bin/env python3

import socket 
import sys

if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise ValueError("Wrong Number of Arguments, Should be 2, but was: " + str(len(sys.argv)))
    if sys.argv[1] == socket.gethostname():
        print("Result: True")
    else:
        print("Result: False")