# NFS
## Qs and As
Can be found on drive, NOT DONE
## Setup

### GW/Router
```IP: 10.0.0.1```
* Nothing this time

### server
```IP: 10.0.0.2```

### client-1
```IP: 10.0.0.3```

### client-2
```IP: 10.0.0.4```

## Tests
* [/tests/check_client_config.py](../6-NFS/tests/check_client_config.py)
    * Can only be ran on a client 
    * Use start_NFS_tests.py to run the whole test suite for NFS
* [/tests/check_server_config.py](../6-NFS/tests/check_server_config.py)
    * Can only be ran on the server 
    * Use start_NFS_tests.py to run the whole test suite for NFS

* [/tests/start_NFS_tests.py](../6-NFS/tests/start_NFS_tests.py)
    * run using `python start_NFS_tests.py [debug]`
    * You have to stand in the tests directory for this to work, no time to fix this

## Adding a user
A script to add a user to the domain has been created. It is ran by `python3 /user_scripts/add_users.py`