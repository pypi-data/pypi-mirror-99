# -*- coding: utf-8 -*-
import requests
import os,json

from .. import wh

def get_requests (api,data="",observed_user_idx=''):
    #observed_user_idx는 myTask의 observe 기능 사용시

    #Observed용 쿠키세팅
    cookies = wh.Login.whtoken.copy()

    if observed_user_idx != "":
        if type(observed_user_idx) == int:
            observed_user_idx = str(observed_user_idx)

        cookies["observed_user_idx"] = '"%s"'%(observed_user_idx)
    request_result = requests.get(wh.Login.url+api, data=data, cookies=cookies)
    json_list = wh_result(request_result)
    return json_list

def post_requests (api,data="",files="",login=""):
    if login =="":

        #파일 읽기 세팅
        files = wh_file_setting(files)
        request_result = requests.post(wh.Login.url+api, files=files,data=data, cookies=wh.Login.whtoken)
        json_list = wh_result(request_result)
        return json_list
    #로그인 사용시
    else:
        request_result = requests.post(wh.Login.url+api,data=data)
        json_list = wh_result(request_result)
        return json_list



# 결과 확인
def wh_result(result):

    if result.status_code == 200:
        json_list = json.loads(result.text)['data']
        # print(json_list)
        # print(json.loads(result.text)['error']['message'])
        return json_list
    else:
        errorcode = "errorcode:"+str(result.status_code)
        print(json.loads(result.text)['error']['message'])
        print(errorcode)
        return result







###############

#딕셔너리 파일 리스트 안에 데이터를 Open해서 리스트 안에 튜플로 반환
def wh_file_setting(file_path_dict):
    file_list =[]
    for key in file_path_dict:
        if type(file_path_dict[key]) == list:
            for file in file_path_dict[key]:
                data = (key,open(file,'rb'))
                file_list.append(data)
                #{a:[1,2,3]} >> [(a,open(1),(a,open(2),(a,open(3)]

        elif type(file_path_dict[key]) == str :
            data = (key, open(file_path_dict[key],'rb'))
            file_list.append(data)

    return file_list
