Control your [Energenie EG-PMS-LAN](https://energenie.com/item.aspx?id=6668) with python.

## geniecli.py CLI

**Usage:**

```
~/energenie-connect0r$ ./geniecli.py --help
usage: geniecli.py [-h] [--status] [--nologout] [--toggle {1,2,3,4}]
                   [--on {1,2,3,4}] [--off {1,2,3,4}] [--restart {1,2,3,4}]
                   [--restartdelaysec RESTARTDELAYSEC]
                   http://192.168.2.5 pwd

positional arguments:
  http://192.168.2.5    Energenie Web URL
  pwd                   Web GUI password

optional arguments:
  -h, --help            show this help message and exit
  --status              fetch socket status
  --nologout            do not logout
  --toggle {1,2,3,4}    toggle socket state
  --on {1,2,3,4}        switch socket on
  --off {1,2,3,4}       switch socket off
  --restart {1,2,3,4}   restart socket
  --restartdelaysec RESTARTDELAYSEC
                        delay between restart off and on
```

**Get device status in JSON format:**

```
~/energenie-connect0r$ ./geniecli.py http://192.168.2.5 passw0rd --status
{"status": true, "data": {"sockets": [1, 0, 1, 1]}, "message": null}
```

**Switch socket with `--on` or `--off`:**

```
~/energenie-connect0r$ ./geniecli.py http://192.168.2.5 passw0rd --on 2
{"status": true, "message": "State of socket 2 changed", "data": {"sockets": [1, 1, 1, 1]}}
```

**Toggle socket (if on then off; if off then on):**

```
~/energenie-connect0r$ ./geniecli.py http://192.168.2.5 passw0rd --toggle 2
{"status": true, "message": "State of socket 2 changed to 0", "data": {"sockets": [1, 0, 1, 1]}}
```

**Restart a socket:**

- Switch socket off
- Wait for RESTARTDELAYSEC seconds
- Switch socket on

```
~/energenie-connect0r$ ./geniecli.py http://192.168.2.5 passw0rd --restart 2 --restartdelaysec 3
{"data": {"sockets": [1, 1, 1, 1]}, "message": "Socket 2 restarted", "status": true}
```

**The `--nologout` option:**

The Energenie allows only one user at the same time.
If you run multiple instances of this script at the same time,
you can use the `--nologout` option to prevent collisions.

```sh
#!/bin/bash

# execute two commands parallel
./geniecli.py http://192.168.2.7 "" --toggle 3 --nologout &
./geniecli.py http://192.168.2.7 "" --toggle 4 --nologout &

# wait for both to finish
wait

# logout
./geniecli.py http://192.168.2.7 "" --logout
```

## geniemassstatus.py CLI

Fetch the socket status from multiple energenie devices:

```
~/energenie-connect0r$ ./geniemassstatus.py --host http://192.168.2.5 --pwd passw0rd --host http://192.168.2.7 --pwd passw0rd
{"http://192.168.2.7": [1, 1, 1, 0], "http://192.168.2.5": [1, 1, 1, 1]}
```

## Python class usage

```py
#!/usr/bin/python3

from energenieconnector import EnergenieConnector

eg = EnergenieConnector("http://192.168.2.5", "")

# Check login state
status = eg.getstatus()

# Login status codes:
# 0 = Logged in
# 1 = Not logged in
# 2 = Login already in use by another user
# 3 = Unknown login result

# Login if not logged in and get status again
if status['login']==1:
    if eg.login():
        status = eg.getstatus()

# Status contains login result and the state of each socket
# {'logintxt': 'Logged in', 'login': 0, 'sockets': [1, 0, 1, 1]}
print(status)

# Change socket state; range: 1-4
# Change state of socket 2 to 'on'
eg.changesocket(2, 1)

# Logout
if status['login']==0:
   eg.logout()
```

