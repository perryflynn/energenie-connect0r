import requests
import sys
import re

class EnergenieConnector:

    def __init__(self, baseurl, pwd):
        self.loginstatustxt = [ "Logged in", "Not logged in", "Login blocked", "Unknown login state" ]
        self.rgx_blocked = "<div>Impossible to login - there is an active session with this device at this moment.</div>"
        self.rgx_login = "<div>&nbsp;EnerGenie Web:&nbsp;.+</div>"
        self.rgx_loggedin = "<div class=\"boxmenuitem\"><a href=\"login\\.html\">Log Out</a></div>"
        self.rgx_socketstates = "var\s+sockstates\s+=\s+\[([01]),([01]),([01]),([01])\];"
        self.baseurl = baseurl
        self.pwd = pwd

    # Fetch state from device
    def getstatus(self):
        r = requests.get(self.baseurl+"/energenie.html")

        if r.status_code==200 and bool(re.search(self.rgx_blocked, r.text)):
            # Login session blocked
            return { "login": 2, "logintxt":self.loginstatustxt[2], "sockets": None }

        elif r.status_code==200 and bool(re.search(self.rgx_login, r.text)):
            # Login required
            return { "login": 1, "logintxt":self.loginstatustxt[1], "sockets": None }

        elif r.status_code==200 and bool(re.search(self.rgx_loggedin, r.text)):
            # Already logged in, fetch socket states
            m = re.search(self.rgx_socketstates, r.text)
            if bool(m):
                return { "login": 0, "logintxt":self.loginstatustxt[0], "sockets": [ int(m.group(1)), int(m.group(2)), int(m.group(3)), int(m.group(4)) ] }
            else:
                return { "login": 0, "logintxt":self.loginstatustxt[0], "sockets": None }

        else:
            # Unknown state
            return { "login": 3, "logintxt":self.loginstatustxt[3], "sockets": None }

    # Perform login
    def login(self):
        r = requests.post(self.baseurl+"/login.html", data={ "pw":self.pwd })
        if r.status_code==200 and bool(re.search(self.rgx_loggedin, r.text)):
            return True
        else:
            return False

    # Perform logout
    def logout(self):
        r = requests.get(self.baseurl+"/login.html")
        if r.status_code==200:
            return True
        else:
            return False

    # Change socket state
    def changesocket(self, socket, state):
        params = { "cte1":"", "cte2":"", "cte3":"", "cte4":"" }
        params['cte'+str(socket)] = state
        r = requests.post(self.baseurl+"/", data=params)
        if r.status_code==200:
            return True
        else:
            return False

