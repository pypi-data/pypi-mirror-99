# -*- coding: utf-8 -*-

import json
import urllib2
import urllib
import random, string, mimetypes

# file Data Type
# file = {"호출키":['file_path','file_path']}

def get_requests(api,data="",observed_user_idx=""):
    from .. import wh

    #데이터 처리
    getdata = urllib.urlencode(data)

    #Get URL생성
    request = urllib2.Request(wh.Login.url + api+'?' + getdata)
    # print(wh.Login.url + api+'?' + getdata)


    # 딕셔너리 헤더를 쿠키 형태로 변경
    headers = header_setting(wh.Login.whtoken)

    if observed_user_idx == "":
        request.add_header('Cookie',headers)

    else:
        #옵져버 세팅
        observed =headers+";observed_user_idx=" + '"%s"'%(observed_user_idx)
        request.add_header('Cookie',observed)

    result_u = urllib2.urlopen(request)
    json_list = wh_result(result_u)


    return json_list

def post_requests(api, data="", files="",login=""):
    from .. import wh


    #로그인 하라는게 아닐때
    if login == "":

        #파일이 없을때
        if files == "":
            #데이터 세팅
            postData = wh_data_setting(data)

            #Request 세팅
            request = urllib2.Request(wh.Login.url + api, data=postData)

            #딕셔너리 헤더를 쿠키 형태로 변경
            headers = header_setting(wh.Login.whtoken)

            #헤더 쿠키 추가
            request.add_header("cookie",headers)


        #파일이 있을때
        else:
            #데이터 인코딩
            postData, file_headers = encode_multipart_data(data, files)

            #헤더 딕셔너리를 세팅
            headers = header_setting(wh.Login.whtoken)

            #request 세팅
            request = urllib2.Request(wh.Login.url + api, data = postData, headers = file_headers)

            #Request세팅에 헤더 추가
            request.add_header('cookie',headers)



    else:
        #로그인
        postData = wh_data_setting(data)
        request = urllib2.Request(wh.Login.url + api, data=postData)

    result_u = urllib2.urlopen(request)
    json_list = wh_result(result_u)
    return json_list

def wh_result(result_u):

    if result_u.getcode() == 200:
        result = result_u.read().decode('UTF-8')
        json_list = json.loads(result)['data']
        # print(json.loads(result)['error']['message'])
        return json_list
    else:
        errorcode = "errorcode"+str(result_u.getcode())
        result = result_u.read().decode('UTF-8')
        print(json.loads(result)['error']['message'])
        print(errorcode)
        return result_u



#########################
#딕셔너리안에 리스트가 있는 데이터 컨버팅
def wh_data_setting(data_dict):
    data =[]
    #data = [key=val,key=val
    for key in data_dict:
        if type(data_dict[key]) == list:
            for data_list in data_dict[key]:
                data.append(urllib.urlencode({key:data_list}))
        else:
            data.append(urllib.urlencode({key:data_dict[key]}))
    return ('&').join(data)


#딕셔너리 헤더를 컨버팅
def header_setting(header_dict):
    cookie = []
    for key in header_dict:
        cookie.append("%s=%s" % (key, header_dict[key]))
    headers = (";").join(cookie)
    return headers


# 멀티파트 인코딩
def random_string(length):
    return ''.join(random.choice (string.letters) for ii in range (length + 1))

def encode_multipart_data(data, files):
    boundary = random_string (30)

    def get_content_type(filename):
        return mimetypes.guess_type(filename)[0] or 'application/octet-stream'

    def encode_field(field_name):
        data_line = []
        data_val= data[field_name]

        #데이터가 리스트로 있는 경우
        if type(data_val) == list:

            for data_pick in data_val :
                data_text = ('--' + boundary,
                             'Content-Disposition: form-data; name="%s"' % field_name,
                             '', str(data_pick))
                data_line.extend(data_text)

        else:
            data_text= ('--' + boundary,
                        'Content-Disposition: form-data; name="%s"' % field_name,
                        '', str(data_val))
            data_line.extend(data_text)

        return data_line



    def encode_file(field_name):
        filename = files [field_name]
        file_line = []

        #파일의 데이터가 복수개 인 경우
        if type(filename) ==list:
            for file_pick in filename:
                data_text = ('--' + boundary,
                        'Content-Disposition: form-data; name="%s"; filename="%s"' % (field_name, file_pick),
                        'Content-Type: %s' % get_content_type(file_pick),
                        '', open(file_pick, 'rb').read())
                file_line.extend(data_text)
        else :
            data_text= ('--' + boundary,
                    'Content-Disposition: form-data; name="%s"; filename="%s"' % (field_name, filename),
                    'Content-Type: %s' % get_content_type(filename),
                    '', open(filename, 'rb').read())
            file_line.extend(data_text)

        return file_line

    lines = []
    for name in data:
        lines.extend(encode_field(name))

    for name in files:
        file_data = encode_file(name)
        lines.extend(file_data)

    lines.extend(('--%s--' % boundary, ''))

    body = '\r\n'.join(lines)

    headers = {'content-type': 'multipart/form-data; boundary=' + boundary,
               'content-length': str(len(body))}
    return body, headers