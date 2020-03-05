import login
import requests
import sys

if __name__ == '__main__':
    requests.packages.urllib3.disable_warnings()
    get_campus = login.AuthserverLogin(sys.argv[1],sys.argv[2])
    get_campus.get_campus()