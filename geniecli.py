#!/usr/bin/python3

import json
import argparse
import sys
import time
from energenieconnector import EnergenieConnector

# Parse command line arguments
def getargs():
    parser = argparse.ArgumentParser()
    parser.add_argument('baseurl', metavar='http://192.168.2.5', type=str, help='Energenie Web URL')
    parser.add_argument('pwd', type=str, help='Web GUI password')
    parser.add_argument('--status', action='store_true', help='fetch socket status')
    parser.add_argument('--logout', action='store_true', help='just log out and exit script')
    parser.add_argument('--nologout', action='store_true', help='do not logout')
    parser.add_argument('--toggle', type=int, choices=range(1,5), help='toggle socket state')
    parser.add_argument('--on', type=int, choices=range(1,5), help='switch socket on')
    parser.add_argument('--off', type=int, choices=range(1,5), help='switch socket off')
    parser.add_argument('--restart', type=int, choices=range(1,5), help='restart socket')
    parser.add_argument('--restartdelaysec', type=int, default=5, help='delay between restart off and on')
    args = parser.parse_args()
    return args


# Main function
def run(args):
    eg = EnergenieConnector(args.baseurl, args.pwd)

    # Check login state
    status = eg.getstatus()

    # Just log out
    if args.logout and status['login']==0:
        eg.logout()
        print(json.dumps({ "status": True, "message": "Logout successful", "data": None }))
        return 0
    
    # Peform login if not logged in
    if status['login']==1:
        if eg.login():
            status = eg.getstatus()
        else:
            print(json.dumps({ "status": False, "message": "Login failed", "data": None }))

    # Get socket states
    if args.status:
        print(json.dumps({ 
            "status": status['login']==0, 
            "message": None if status['login']==0 else status['logintxt'], 
            "data": { "sockets": status['sockets'] } 
        }))

    # Switch socket on or off
    elif args.on is not None or args.off is not None:
        targetstate = 1 if args.on is not None else 0
        targetsocket = args.on if args.on is not None else args.off

        if targetstate!=status['sockets'][targetsocket-1]:
            # Perform socket state change
            eg.changesocket(targetsocket, targetstate)
            status = eg.getstatus()
            print(json.dumps({ 
                "status": status.get("login")==0, 
                "message": "State of socket "+str(targetsocket)+" changed", 
                "data": { "sockets": status.get("sockets") } 
            }))
        else:
            # No change necessary
            print(json.dumps({ 
                "status": False, 
                "message": "State of socket "+str(targetsocket)+" is already "+str(targetstate), 
                "data": { "sockets": status.get("sockets") }
            }))

    # Toggle socket
    elif args.toggle is not None:
        targetstate = 1 if status['sockets'][args.toggle-1]==0 else 0
        targetsocket = args.toggle
        eg.changesocket(targetsocket, targetstate)
        status = eg.getstatus()
        print(json.dumps({
            "status": status.get("login")==0,
            "message": "State of socket "+str(targetsocket)+" changed to "+str(targetstate),
            "data": { "sockets": status.get("sockets") }
        }))

    # Restart socket
    elif args.restart is not None:
        sock = args.restart
        if status['sockets'][sock-1]==1:
            eg.changesocket(sock, 0)
            time.sleep(args.restartdelaysec)
        eg.changesocket(sock, 1)

        status = eg.getstatus()
        print(json.dumps({
            "status": status.get("login")==0,
            "message": "Socket "+str(sock)+" restarted",
            "data": { "sockets": status.get("sockets") }
        }))

    # No action
    else:
       print(json.dumps({ "status":False, "message":"Nothing to do", "data":{ "sockets": status.get("sockets") } }))


    # Logout
    if status.get("login")==0 and args.nologout==False:
        eg.logout()

    return 0


# Parse arguments and run main function
if __name__ == "__main__":
    shellargs = getargs()
    result = run(shellargs)
    sys.exit(result)

