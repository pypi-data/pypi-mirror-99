# -*- coding: utf-8 -*-
import os


#### import test
try:
    from . import wh_requests as wh_rest_api
    print('use Requests Module')

except ImportError:
    try:
        from . import wh_urllib3 as wh_rest_api
        print('use urllib3 library')

    except ImportError:
        try:
            from . import wh_urllib2 as wh_rest_api
            print('use urllib2 library')

        except ImportError:
            print("module Import error")

def get_requests (api,data="",observed_user_idx=''):
    result = wh_rest_api.get_requests(api=api,data = data ,observed_user_idx = observed_user_idx)
    return result


def post_requests (api,data="",files="",login=""):
    result = wh_rest_api.post_requests(api=api, data=data,files=files,login=login)
    return result


def file_folder_check(path_list):
    file_list = []
    folder_list=[]
    for path in path_list:
        if os.path.isfile(path):
            file_list.append(path)
        elif os.path.isdir(path):
            folder_list.append(path)
        else:
            print('확인 불가능: ',path)

    if file_list ==[] and folder_list == []:
        return None
    else:
        return {"file":file_list,"folder":folder_list}
