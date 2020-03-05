import login
import requests
import sys
import time
import re
import json

if __name__ == '__main__':
    requests.packages.urllib3.disable_warnings()
    get_class = login.AuthserverLogin(sys.argv[1], sys.argv[2])
    t1 = time.time()
    a = get_class.get_class()
    a = json.loads(a)
    print(a)
    print(len(a))
    t2 = time.time()
    print('花费时间:{}s'.format(t2-t1))

