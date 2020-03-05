import login
import requests
import sys
import json
import time

if __name__ == '__main__':
    requests.packages.urllib3.disable_warnings()
    get_grade = login.AuthserverLogin(sys.argv[1],sys.argv[2])
    t1 = time.time()
    grade = get_grade.get_grades()
    grade = json.loads(grade)
    print(grade)
    print(len(grade))
    t2 = time.time()
    print('花费时间:{}s'.format(t2-t1))
