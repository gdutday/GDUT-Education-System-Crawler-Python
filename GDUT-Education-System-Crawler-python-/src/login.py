# -*- coding: utf-8 -*-
import requests
from lxml import etree
from bs4 import BeautifulSoup
import re
import json
import sys
import codecs
sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())



class AuthserverLogin:
    login_url = 'http://authserver.gdut.edu.cn/authserver/login?service=http%3A%2F%2Fjxfw.gdut.edu.cn%2Fnew%2FssoLogin'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'
    }

    def __init__(self,username,password):
        self.username = username
        self.password = password
        self._session = requests.session()
        self._session.headers = self.headers
        self.login()

    def get_post_data(self):
        post_data = dict()
        html = etree.HTML(self._session.get(self.login_url,verify=False).text)
        key = html.xpath('.//input[@type="hidden"]/@name')
        value = html.xpath('.//input[@type="hidden"]/@value')
        for key, value in zip(key, value):
            post_data[key] = value
        post_data['username'] = self.username
        post_data['password'] = self.password
        return post_data

    def login(self):
        dom = etree.HTML(self._session.post(self.login_url, data=self.get_post_data(),verify=False).text)
        result = dom.xpath('//*[@id="msg"]/text()')
        if any(result):
            print(result[0])
            exit()

    # 获取课表版本一： 通过设置过量的rows直接获取全部数据
    def get_class(self):
        class_url = 'https://jxfw.gdut.edu.cn/xsgrkbcx!getDataList.action'
        post_data = {
            'zc': '',
            'xnxqdm': '201901',
            'page': '1',
            'rows': '1000',
            'sort': 'kxh',
            'order': 'asc'
        }
        response = self._session.post(class_url, verify=False, data=post_data)
        result = json.loads(response.text)
        person_classes = result['rows']
        person_classes = str(person_classes)
        person_classes = re.sub('kcmc', 'courseName', person_classes)  # 课程名称
        person_classes = re.sub('sknrjj', 'courseContent', person_classes)  # 授课内容
        person_classes = re.sub('jcdm', 'courseTime', person_classes)  # 课程节次
        person_classes = re.sub('zc', 'courseWeek', person_classes)  # 课程周次
        person_classes = re.sub('xq', 'courseDay', person_classes)  # 课程日
        person_classes = re.sub('jxcdmc', 'courseRoom', person_classes)  # 课程地点
        person_classes = re.sub('teaxms', 'courseTeacher', person_classes)  # 课程教师
        person_classes = re.sub("'dgksdm': '.*?', ", '', person_classes)
        person_classes = re.sub("'pkrs': '.*?', ", '', person_classes)
        person_classes = re.sub("'kxh': '.*?', ", '', person_classes)
        person_classes = re.sub("'jxhjmc': '.*?', ", '', person_classes)
        person_classes = re.sub("'flfzmc': '.*?', ", '', person_classes)
        person_classes = re.sub("'pkrq': '.*?', ", '', person_classes)
        person_classes = re.sub("'rownum_': '.*?'", '', person_classes)
        person_classes = re.sub("'jxbmc': '.*?', ", '', person_classes)
        person_classes = re.sub(', }', '}', person_classes)
        person_classes = re.sub("'", '"', person_classes)
        # person_classes = person_classes.encode(encoding='UTF-8').decode(encoding='UTF-8')
        print(person_classes)
        return person_classes

    # 获取课表版本二：显示全部课程，再进行翻页获取数据版本
    # def get_class(self):
    #     class_url = 'https://jxfw.gdut.edu.cn/xsgrkbcx!getDataList.action'
    #     post_data = {
    #         'zc': '',
    #         'xnxqdm': '201901',
    #         'page': '1',
    #         'rows': '20',
    #         'sort': 'kxh',
    #         'order': 'asc'
    #     }
    #     response = self._session.post(class_url, verify=False, data=post_data)
    #     result = json.loads(response.text)
    #     page_number = result['total'] // 20 + 1
    #     person_classes = result['rows']
    #     if page_number != 1:
    #         for i in range(2, page_number + 1):
    #             post_data['page'] = str(i)
    #             resp = self._session.post(class_url, verify=False, data=post_data)
    #             res = json.loads(resp.text)
    #             person_classes.extend(res['rows'])
    #     person_classes = str(person_classes)
    #     # person_classes = re.sub('kcmc', 'courseName', person_classes)  # 课程名称
    #     # person_classes = re.sub('sknrjj', 'courseContent', person_classes)  # 授课内容
    #     # person_classes = re.sub('jcdm', 'courseTime', person_classes)  # 课程节次
    #     # person_classes = re.sub('zc', 'courseWeek', person_classes)  # 课程周次
    #     # person_classes = re.sub('xq', 'courseDay', person_classes)  # 课程日
    #     # person_classes = re.sub('jxcdmc', 'courseRoom', person_classes)  # 课程地点
    #     # person_classes = re.sub('teaxms', 'courseTeacher', person_classes)  # 课程教师
    #     # person_classes = re.sub("'dgksdm': '.*?', ", '', person_classes)
    #     # person_classes = re.sub("'pkrs': '.*?', ", '', person_classes)
    #     # person_classes = re.sub("'kxh': '.*?', ", '', person_classes)
    #     # person_classes = re.sub("'jxhjmc': '.*?', ", '', person_classes)
    #     # person_classes = re.sub("'flfzmc': '.*?', ", '', person_classes)
    #     # person_classes = re.sub("'pkrq': '.*?', ", '', person_classes)
    #     # person_classes = re.sub("'rownum_': '.*?'", '', person_classes)
    #     # person_classes = re.sub("'jxbmc': '.*?', ", '', person_classes)
    #     # person_classes = re.sub(', }', '}', person_classes)
    #     person_classes = re.sub("'", '"', person_classes)
    #     # # person_classes = person_classes.encode(encoding='UTF-8').decode(encoding='UTF-8')
    #     # print(person_classes)
    #     return person_classes

    # 获取课表版本三： 按周次遍历，获取数据版本
    # def get_class(self):
    #     class_url = 'https://jxfw.gdut.edu.cn/xsgrkbcx!getDataList.action'
    #     post_data = {
    #         'zc': '1',
    #         'xnxqdm': '201901',
    #         'page': '1',
    #         'rows': '40',
    #         'sort': 'kxh',
    #         'order': 'asc'
    #     }
    #     person_classes = []
    #     for i in range(1,23):
    #         post_data['zc'] = str(i)
    #         response = self._session.post(class_url, verify=False, data=post_data)
    #         result = json.loads(response.text)
    #         print(result)
    #         print(i,'='*100)
    #         person_classes.extend(result['rows'])
    #     post_data['zc'] = ''
    #     response = self._session.post(class_url, verify=False, data=post_data)
    #     result = json.loads(response.text)
    #     print(result['total'])
    #     print(len(person_classes))
        # person_classes = str(person_classes)
        # person_classes = re.sub('kcmc', 'courseName', person_classes)  # 课程名称
        # person_classes = re.sub('sknrjj', 'courseContent', person_classes)  # 授课内容
        # person_classes = re.sub('jcdm', 'courseTime', person_classes)  # 课程节次
        # person_classes = re.sub('zc', 'courseWeek', person_classes)  # 课程周次
        # person_classes = re.sub('xq', 'courseDay', person_classes)  # 课程日
        # person_classes = re.sub('jxcdmc', 'courseRoom', person_classes)  # 课程地点
        # person_classes = re.sub('teaxms', 'courseTeacher', person_classes)  # 课程教师
        # person_classes = re.sub("'dgksdm': '.*?', ", '', person_classes)
        # person_classes = re.sub("'pkrs': '.*?', ", '', person_classes)
        # person_classes = re.sub("'kxh': '.*?', ", '', person_classes)
        # person_classes = re.sub("'jxhjmc': '.*?', ", '', person_classes)
        # person_classes = re.sub("'flfzmc': '.*?', ", '', person_classes)
        # person_classes = re.sub("'pkrq': '.*?', ", '', person_classes)
        # person_classes = re.sub("'rownum_': '.*?'", '', person_classes)
        # person_classes = re.sub("'jxbmc': '.*?', ", '', person_classes)
        # person_classes = re.sub(', }', '}', person_classes)
        # person_classes = re.sub("'", '"', person_classes)
        # person_classes = person_classes.encode(encoding='UTF-8').decode(encoding='UTF-8')
        # print(person_classes)
        # return person_classes


    def get_grades(self):
        grade_url = 'https://jxfw.gdut.edu.cn/xskccjxx!getDataList.action'
        post_data = {
            'xnxqdm':'',
            'jhlxdm':'',
            'page':'1',
            'rows':'1000',
            'sort':'xnxqdm',
            'order':'asc'
        }
        response = self._session.post(grade_url,verify=False,data=post_data)
        result = json.loads(response.text)
        person_grades = result['rows']
        person_grades = str(person_grades)
        person_grades = re.sub('xnxqmc','examTime',person_grades)           #考试时间
        person_grades = re.sub("cjjd", 'examPole', person_grades)         #考试绩点
        person_grades = re.sub('zcj', 'examScore', person_grades)           #考试分数
        person_grades = re.sub('kcmc', 'examName', person_grades)           #考试科目
        person_grades = re.sub('xf', 'credit', person_grades)   # 考试学分
        person_grades = re.sub("'rownum_': '.*?', ", '', person_grades)
        person_grades = re.sub("'isactive': '.*?', ", '', person_grades)
        person_grades = re.sub(" 'wpjbz': '.*?', ", '', person_grades)
        person_grades = re.sub("'kcflmc': '.*?', ", '', person_grades)
        person_grades = re.sub("'xsxm': '.*?',", '', person_grades)
        person_grades = re.sub("'ksxzdm': '.*?', ", '', person_grades)
        person_grades = re.sub("'kcdm': '.*?', ", '', person_grades)
        person_grades = re.sub("'bz': '.*?', ", '', person_grades)
        person_grades = re.sub("'cjdm': '.*?', ", '', person_grades)
        person_grades = re.sub("'wzc': '.*?', ", '', person_grades)
        person_grades = re.sub("'ksxzmc': '.*?', ", '', person_grades)
        person_grades = re.sub("'cjbzmc': '.*?', ", '', person_grades)
        person_grades = re.sub("'kcbh': '.*?', ", '', person_grades)
        person_grades = re.sub("'wpj': '.*?', ", '', person_grades)
        person_grades = re.sub("'xdfsmc': '.*?', ", '', person_grades)
        person_grades = re.sub("'xsbh': '.*?', ", '', person_grades)
        person_grades = re.sub("'zxs': '.*?', ", '', person_grades)
        person_grades = re.sub("'xnxqdm': '.*?', ", '', person_grades)
        person_grades = re.sub("'kcdlmc': '.*?', ", '', person_grades)
        person_grades = re.sub("'cjfsmc': '.*?'", '', person_grades)
        person_grades = re.sub("'wzcbz': '.*?', ", '', person_grades)
        person_grades = re.sub("'xsdm': '.*?', ", '', person_grades)
        person_grades = re.sub("'rwdm': '.*?', ", '', person_grades)
        person_grades = re.sub(', }', '}', person_grades)
        person_grades = re.sub("'", '"', person_grades)
        # person_grades = person_grades.encode(encoding='UTF-8').decode(encoding='UTF-8')
        # print(person_grades)
        return person_grades





    def get_exam(self):
        post_url = 'https://jxfw.gdut.edu.cn/xsksap!getDataList.action'
        post_data = {
            'xnxqdm':'201901',
            'ksaplxdm':'',
            'page':1,
            'rows':'1000',
            'sort':'zc,xq,jcdm2',
            'order':'asc'
        }
        response = self._session.post(post_url,data=post_data,verify=False)
        result = json.loads(response.text)
        person_exam = result['rows']
        person_exam = str(person_exam)
        person_exam = re.sub('ksrq','examDate',person_exam)        # 考试日期
        person_exam = re.sub('zc', 'examWeek', person_exam)        # 考试周次
        person_exam = re.sub('xq', 'examDay', person_exam)         # 考试日
        person_exam = re.sub('kssj', 'examTime', person_exam)      # 考试时间
        person_exam = re.sub('zwh', 'examPosition', person_exam)   # 考试座位号
        person_exam = re.sub('kcmc', 'examSubject', person_exam)   # 考试科目
        person_exam = re.sub('kscdmc', 'examClassroom', person_exam)  # 考试地点
        person_exam = re.sub("'ksrcdm': '.*?', ", '', person_exam)
        person_exam = re.sub("'xsbh': '.*?', ", '', person_exam)
        person_exam = re.sub("'kslbmc': '.*?', ", '', person_exam)
        person_exam = re.sub("'jcdm2': '.*?', ", '', person_exam)
        person_exam = re.sub("'jkteaxms': '.*?', ", '', person_exam)
        person_exam = re.sub("'xs': '.*?', ", '', person_exam)
        person_exam = re.sub("'examDaymc': '.*?', ", '', person_exam)
        person_exam = re.sub("'ksaplxmc': '.*?', ", '', person_exam)
        person_exam = re.sub("'kcbh': '.*?', ", '', person_exam)
        person_exam = re.sub("'sjbh': '.*?', ", '', person_exam)
        person_exam = re.sub("'ksxs': '.*?', ", '', person_exam)
        person_exam = re.sub("'rownum_': '.*?'", '', person_exam)
        person_exam = re.sub("'xnexamDaydm': '.*?', ", '', person_exam)
        person_exam = re.sub("'xsxm': '.*?', ", '', person_exam)
        person_exam = re.sub(", }", '}', person_exam)
        person_exam = re.sub("'", '"', person_exam)
        # person_exam = person_exam.encode(encoding='UTF-8').decode(encoding='UTF-8')
        print(person_exam)
        return  person_exam

    def get_campus(self):
        get_url = 'https://jxfw.gdut.edu.cn/xjkpxx!xjkpxx.action'
        response = self._session.get(get_url,verify=False)
        result = response.text
        soup = BeautifulSoup(result,'lxml')
        campus = soup.find_all(text=re.compile('校区'))[-1]
        res = str({'所在校区':campus})
        res = re.sub("'", '"',res)
        print(res)

#
# if __name__ == '__main__':
#     # AuthserverLogin(sys.argv[1],sys.argv[2])
#     requests.packages.urllib3.disable_warnings()
