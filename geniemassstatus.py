#!/usr/bin/python3

import json
import argparse
import sys
from energenieconnector import EnergenieConnector

# Parse command line arguments
def getargs():
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', metavar='http://192.168.2.5', action='append', help='Host', required=True)
    parser.add_argument('--pwd', metavar='pwd', action='append', help='Web GUI password', required=True)
    parser.add_argument('--nologout', action='store_true', help='do not logout')
    args = parser.parse_args()
    return args


# Main function
def run(args):
    status = {}

    for i in range(0,len(args.host)):
        eg = EnergenieConnector(args.host[i], args.pwd[i])
        curstatus = eg.getstatus()
        if curstatus['login']==1:
            eg.login()

        status[args.host[i]] = eg.getstatus()['sockets']

        if args.nologout==False:
            eg.logout()

    print(json.dumps(status))
    return 0


# Parse arguments and run main function
if __name__ == "__main__":
    shellargs = getargs()
    result = run(shellargs)
    sys.exit(result)

