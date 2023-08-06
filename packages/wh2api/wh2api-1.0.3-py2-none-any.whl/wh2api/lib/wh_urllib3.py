# -*- coding: utf-8 -*-

import json
import urllib3
import urllib
import random, string, mimetypes
import os

def get_requests(api,data="",observed_user_idx=""):
    from .. import wh

    #urllib3 세팅
    http = urllib3.PoolManager()

    #데이터 처리
    getdata = urllib3.request.urlencode(data)
    # print(getdata)

    #토큰 처리
    wh_token = header_setting(wh.Login.whtoken)

    if observed_user_idx == "":
        # Get URL생성
        result = http.request('Get', url=wh.Login.url + api + '?'+ getdata, headers={"cookie":wh_token})

    else:
        #옵져버 세팅
        observed =wh_token+";observed_user_idx=" + '"%s"'%(observed_user_idx)
        # Get URL생성
        result = http.request('Get', url=wh.Login.url + api + '?'+ getdata, headers={"cookie": observed})

    json_list = wh_result(result)
    return json_list

def post_requests(api, data="", files="",login=""):
    from .. import wh

    # urllib3 세팅
    http = urllib3.PoolManager()
    header =[]

    #로그인이 아님
    if login == "":
        #파일이 있는 경우
        if files !="":
            #웜홀 토큰 세팅
            wh_token = ("cookie",header_setting(wh.Login.whtoken))
            header.append(wh_token)

            # 파일 데이터 세팅
            file_data = file_setting(files)

            #포스트 데이터 세팅
            postData = wh_data_setting(data)

            #파일 데이터 추가
            postData.extend((file_data))

            result = http.request("POST", url=wh.Login.url + api, fields=postData, headers=header)

        #파일이 없는 경우

        else:
            #웜홀 토큰 세팅
            wh_token = ("cookie",header_setting(wh.Login.whtoken))
            header.append(wh_token)

            # 데이터 세팅
            postData = wh_data_setting(data)
            result = http.request("POST", url=wh.Login.url + api, fields=postData, headers=header)

    # 로그
    else:
        #로그인
        result = http.request("POST", url = wh.Login.url + api, fields =data)

    json_list = wh_result(result)
    return json_list

def wh_result(result_u):
    # print(result_u.status)
    # print(result_u.data)
    if result_u.status == 200:
        try:
            result = json.loads(result_u.data.decode('utf-8'))
        except:
            print(result_u.data)
            result = json.loads(result_u.data)
        json_list = result['data']
        # print(result['error']['message'])
        return json_list
    else:
        errorcode = "errorcode"+str(result_u.status)
        result = json.loads(result_u.data.decode('utf-8'))
        print(result['error']['message'])
        print(errorcode,)
        return result_u


#########################
#딕셔너리안에 리스트가 있는 데이터 컨버팅
def wh_data_setting(data_dict):
    data =[]
    #data = [(key,val),(key,val)]
    for key in data_dict:
        if type(data_dict[key]) == list:
            for data_list in data_dict[key]:
                inputdata = (key,str(data_list))
                data.append(inputdata)
                # data.append({key:data_list})
        else:
            inputdata = (key, str(data_dict[key]))
            data.append(inputdata)
            # data.append({key:data_dict[key]})
    return data

#딕셔너리 헤더를 컨버팅
def header_setting(header_dict):
    cookie = []
    #cookie=[("key"="val")
    for key in header_dict:
        cookie.append("%s=%s" % (key, header_dict[key]))
    headers = (";").join(cookie)
    return headers


# 멀티파트 인코딩
def file_setting(files):

    def get_content_type(filename):
        return mimetypes.guess_type(filename)[0] or 'application/octet-stream'

    def file_conv(key):
        file_conv_data = []
        #file_conv_data =[(key,(filename,data_read,file_type)),(key,(filename,data_read,file_type))]
        #file이 리스트인 경우
        if type(files[key]) == list:
            for file in files[key]:
                file_name = os.path.basename(file)
                file_open = open(file,'rb').read()
                file_type = get_content_type(file)

                pick_file_data = (key, (file_name, file_open, file_type))
                file_conv_data.append(pick_file_data)

        #file이 리스트가 아닌 경우
        else:
            file_name = os.path.basename(files[key])
            file_open = open(files[key], 'rb').read()
            file_type = get_content_type(files[key])

            pick_file_data = (key,(file_name,file_open,file_type))
            file_conv_data.append(pick_file_data)

        return file_conv_data



    file_data = []
    for key in files:
        file_data.extend(file_conv(key))

    return file_data