# -*- coding: utf-8 -*-

from . import wh_setting, api_list

def list(project_idx,category_idx="all"):
    if category_idx == "all":
        api = api_list.asset_bulk_list %(project_idx)
    else:
        api = api_list.asset_list %(project_idx,category_idx)

    result = wh_setting.get_requests(api=api)
    return result

def create(project_idx,category_idx,asset_name,description="",status_idx="1"):
    api = api_list.asset_create %(project_idx,category_idx)
    data = {"asset_name":asset_name,"description":description,"status_idx":status_idx}
    result = wh_setting.post_requests(api=api,data=data)
    return result

def bulk_create(project_idx,category_name=[],asset_name=[],description=[]):
    api = api_list.asset_bulk_create %(project_idx)

    data = {"category_name[]": category_name, "asset_name[]": asset_name, "description[]": description}


    # 데이터 유효성 체크

    # 리스트의 길이가 다 같은지 체크
    if len(category_name) == len(asset_name) == len(description) :
        pass

    else:

        # 리스트 갑중에 제일 긴 숫자를 구
        max_length = len(max(category_name, asset_name, description))
        for input_key in data:
            if max_length != len(data[input_key]):
                print(input_key + "의 데이터가 부족 합니다.")
            else:
                pass
        return ""

    result = wh_setting.post_requests(api=api, data=data)
    return result


def thumbnail_update(project_idx,asset_idx,thumbnail_path):
    api = api_list.asset_thumbnail_up %(project_idx,asset_idx)
    # thumbnail = open(thumbnail_path,'rb')
    files = {"attached":thumbnail_path}
    result = wh_setting.post_requests(api=api,files=files)
    return result

def overview(project_idx,category_idx=""):
    if category_idx == "":
        api = api_list.asset_overview_all %(project_idx)
    else :
        api = api_list.asset_overview_category %(project_idx,category_idx)
    result = wh_setting.get_requests(api=api)
    return result