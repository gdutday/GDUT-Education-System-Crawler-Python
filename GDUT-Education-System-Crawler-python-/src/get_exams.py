import login
import requests
import sys
import json
import time

if __name__ == '__main__':
    requests.packages.urllib3.disable_warnings()
    get_exam = login.AuthserverLogin(sys.argv[1],sys.argv[2])
    t1 = time.time()
    exam = get_exam.get_exam()
    exam = json.loads(exam)
    # print(exam)
    # print(len(exam))
    t2 = time.time()
    print('花费时间:{}s'.format(t2-t1))

