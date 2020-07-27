#!/usr/bin/env python3

import pexpect
from datetime import datetime

if __name__ == "__main__":
    
    # Testing connectivity to NTP Server
    child = pexpect.spawn("ntpdate -q 10.0.0.1")
    child.expect(pexpect.EOF or pexpect.TIMEOUT)
    result = str(child.before.rstrip().decode("utf-8"))
    assert("server 10.0.0.1, stratum" in result)

    # Testing sync to NTP server
    child = pexpect.spawn("ntpstat")
    child.expect(pexpect.EOF or pexpect.TIMEOUT)
    result = str(child.before.rstrip().decode("utf-8"))
    assert("synchronised to NTP server (10.0.0.1)" in result)
    
    # Screwing up time and checking whether ntp fixes it
    current_date = datetime.now()
    child = pexpect.spawn("date -s \"1 year\"")
    child.expect("" + str(current_date.year + 1) or pexpect.TIMEOUT)
    wrong_date = datetime.now()

    # Resetting NTP service and sync 
    child = pexpect.spawn("service ntp stop")
    child.expect(pexpect.EOF or pexpect.TIMEOUT)
    child = pexpect.spawn("ntpd -gq >/dev/null")
    child.expect(pexpect.EOF or pexpect.TIMEOUT)
    child = pexpect.spawn("service ntp start >/dev/null")
    child.expect(pexpect.EOF or pexpect.TIMEOUT)

    # Checking date is fixed
    fixed_date = datetime.now()
    assert(current_date.month == fixed_date.month and current_date.year == fixed_date.year)
    print("PASSED")


